from typing import Any, Optional

from aiohuesyncbox.controllers.behavior import Behavior
from aiohuesyncbox.controllers.device import Device
from aiohuesyncbox.controllers.execution import Execution
from aiohuesyncbox.controllers.hue import Hue
from aiohuesyncbox.models import (
    BehaviorData,
    DeviceData,
    ExecutionData,
    ExecutionMode,
    HdmiSource,
    HueData,
    LedMode,
    Registration,
    RegistrationCredentials,
)
from aiohuesyncbox.controllers.registrations import Registrations


def _device_raw(led_mode: int = 1) -> dict:
    return {
        "name": "My Sync Box",
        "deviceType": "HSB1",
        "uniqueId": "C42996000000",
        "apiLevel": 7,
        "firmwareVersion": "1.7.4",
        "buildNumber": 1,
        "ipAddress": "192.168.1.12",
        "ledMode": led_mode,
    }


def _device_data(led_mode: int = 1) -> DeviceData:
    return DeviceData.from_dict(_device_raw(led_mode))



class FakeRequest:
    """Records calls and returns canned responses, standing in for HueSyncBox.request."""

    def __init__(self) -> None:
        self.calls: list[tuple] = []
        self.response: Optional[dict[str, Any]] = None

    async def __call__(self, method, path, data=None, auth=True):
        self.calls.append((method, path, data))
        return self.response


async def test_resource_delegates_field_access_to_data():
    device = Device(_device_data(), FakeRequest())

    assert device.name == "My Sync Box"
    assert device.led_mode is LedMode.REGULAR


async def test_resource_mutation_calls_put_on_correct_path():
    request = FakeRequest()
    device = Device(_device_data(), request)

    await device.set_led_mode(LedMode.DIMMED)

    assert request.calls == [("put", "/device", {"ledMode": 2})]


async def test_resource_refresh_replaces_underlying_data():
    request = FakeRequest()
    device = Device(_device_data(led_mode=1), request)
    request.response = _device_raw(led_mode=2)

    await device.refresh()

    assert request.calls == [("get", "/device", None)]
    assert device.led_mode is LedMode.DIMMED


async def test_execution_set_state_serializes_enum_values():
    request = FakeRequest()
    execution = Execution(
        ExecutionData.from_dict(
            {
                "syncActive": False,
                "hdmiActive": True,
                "mode": "passthrough",
                "lastSyncMode": "video",
                "hdmiSource": "input1",
                "hueTarget": "groups/1",
                "brightness": 100,
                "video": {"intensity": "moderate", "backgroundLighting": True},
                "game": {"intensity": "moderate", "backgroundLighting": True},
                "music": {"intensity": "moderate", "palette": "neutral"},
            }
        ),
        request,
    )

    await execution.set_state(
        sync_active=True,
        mode=ExecutionMode.VIDEO,
        hdmi_source=HdmiSource.INPUT3,
    )

    assert request.calls == [
        (
            "put",
            "/execution",
            {"syncActive": True, "mode": "video", "hdmiSource": "input3"},
        )
    ]


def test_hue_groups_iterate_groups_with_id_lookup():
    hue = Hue(
        HueData.from_dict(
            {
                "bridgeUniqueId": "001788FFFE000000",
                "bridgeIpAddress": "192.168.1.8",
                "connectionState": "connected",
                "groups": {
                    "area-id": {
                        "name": "TV Area",
                        "numLights": 5,
                        "active": False,
                    }
                },
            }
        ),
        FakeRequest(),
    )

    assert [group.name for group in hue.groups] == ["TV Area"]
    assert hue.groups_by_id["area-id"].id == "area-id"


async def test_force_dovi_native_uses_boolean_controller_api():
    request = FakeRequest()
    behavior = Behavior(
        BehaviorData.from_dict(
            {
                "inactivePowersave": 20,
                "cecPowersave": 1,
                "usbPowersave": 1,
                "hpdInputSwitch": 1,
            }
        ),
        request,
    )

    await behavior.set_force_dovi_native(True)
    await behavior.set_force_dovi_native(False)

    assert request.calls == [
        ("put", "/behavior", {"forceDoviNative": 1}),
        ("put", "/behavior", {"forceDoviNative": 0}),
    ]



async def test_collection_resource_loads_items_keyed_by_id():
    request = FakeRequest()
    registrations = Registrations(request)

    registrations.load(
        {
            "0": {
                "appName": "Hue Sync Android",
                "instanceName": "Pixel",
                "role": "admin",
                "lastUsed": "2020-02-16T05:45:20Z",
                "created": "2020-01-11T05:45:20Z",
            }
        }
    )

    assert len(registrations) == 1
    registration = registrations["0"]
    assert isinstance(registration, Registration)
    assert registration.id == "0"
    assert registration.app_name == "Hue Sync Android"


async def test_collection_resource_refresh_clears_items_for_empty_response():
    request = FakeRequest()
    registrations = Registrations(request)
    registrations.load(
        {
            "0": {
                "appName": "Hue Sync Android",
                "instanceName": "Pixel",
                "role": "admin",
                "lastUsed": "2020-02-16T05:45:20Z",
                "created": "2020-01-11T05:45:20Z",
            }
        }
    )
    request.response = {}

    await registrations.refresh()

    assert len(registrations) == 0


async def test_collection_resource_delete_calls_correct_path():
    request = FakeRequest()
    registrations = Registrations(request)

    await registrations.delete("0")

    assert request.calls == [("delete", "/registrations/0", None)]


async def test_registration_create_returns_typed_credentials():
    request = FakeRequest()
    request.response = {
        "registrationId": "registration-id",
        "accessToken": "access-token",
    }
    registrations = Registrations(request)

    credentials = await registrations.create("Home Assistant", "Kitchen")

    assert credentials == RegistrationCredentials(
        registration_id="registration-id", access_token="access-token"
    )
    assert request.calls == [
        (
            "post",
            "/registrations",
            {"appName": "Home Assistant", "instanceName": "Kitchen"},
        )
    ]
