import json

from aiohuesyncbox.models import (
    BehaviorData,
    ConnectionState,
    DeviceAction,
    DeviceData,
    ExecutionData,
    ExecutionMode,
    HdmiSource,
    HdmiData,
    HueData,
    Intensity,
    LedMode,
    MusicPalette,
    ExecutionUpdate,
    HueUpdate,
    PortStatus,
    PortType,
    Registration,
    RegistrationRole,
    SyncMode,
    WifiState,
    WifiStrength,
)

EXAMPLE_CONFIG = """
{
    "device": {
        "name": "My Sync Box",
        "deviceType": "HSB1",
        "uniqueId": "C42996000000",
        "apiLevel": 7,
        "firmwareVersion": "1.7.4",
        "buildNumber": 681947148,
        "wifiState": "wan",
        "ipAddress": "192.168.1.12",
        "wifi": {
            "ssid": "Wifi_2G",
            "strength": 4
        },
        "lastCheckedUpdate": "2020-02-16T11:17:13Z",
        "updatableBuildNumber": null,
        "updatableFirmwareVersion": null,
        "update": {
            "autoUpdateEnabled": true,
            "autoUpdateTime": 11
        },
        "ledMode": 1,
        "action": "none",
        "pushlink": "idle",
        "capabilities": {
            "maxIrCodes": 24,
            "maxPresets": 16
        }
    },
    "hue": {
        "bridgeUniqueId": "001788FFFE000000",
        "bridgeIpAddress": "192.168.1.8",
        "groups": {
            "db7dd240-d061-48bf-84c2-01f086e4bfae": {
                "name": "TV Area",
                "numLights": 5,
                "active": false
            },
            "f7bd7dcb-bbcb-4cd1-b343-126e60575884": {
                "name": "PC Area",
                "numLights": 4,
                "active": false
            }
        },
        "connectionState": "connected"
    },
    "execution": {
        "mode": "powersave",
        "syncActive": false,
        "hdmiActive": false,
        "hdmiSource": "input1",
        "hueTarget": "db7dd240-d061-48bf-84c2-01f086e4bfae",
        "brightness": 122,
        "lastSyncMode": "video",
        "video": {
            "intensity": "moderate",
            "backgroundLighting": true
        },
        "game": {
            "intensity": "high",
            "backgroundLighting": false
        },
        "music": {
            "intensity": "high",
            "palette": "melancholicEnergetic"
        },
        "preset": null
    }
}
"""


def _data():
    return json.loads(EXAMPLE_CONFIG)


def test_device_from_dict():
    device = DeviceData.from_dict(_data()["device"])

    assert device.name == "My Sync Box"
    assert device.device_type == "HSB1"
    assert device.unique_id == "C42996000000"
    assert device.led_mode is LedMode.REGULAR
    assert device.wifi_state is WifiState.WAN
    assert device.action is DeviceAction.NONE
    assert device.wifi is not None
    assert device.wifi.ssid == "Wifi_2G"
    assert device.wifi.strength is WifiStrength.EXCELLENT


def test_device_to_dict_round_trips_camel_case():
    device = DeviceData.from_dict(_data()["device"])

    as_dict = device.to_dict()

    assert "ledMode" in as_dict
    assert "led_mode" not in as_dict
    assert as_dict["wifi"] == {"ssid": "Wifi_2G", "strength": 4}


def test_execution_from_dict():
    execution = ExecutionData.from_dict(_data()["execution"])

    assert execution.sync_active is False
    assert execution.mode is ExecutionMode.POWERSAVE
    assert execution.last_sync_mode is SyncMode.VIDEO
    assert execution.hdmi_source is HdmiSource.INPUT1
    assert execution.hue_target == "db7dd240-d061-48bf-84c2-01f086e4bfae"
    assert execution.video.intensity is Intensity.MODERATE
    assert execution.video.background_lighting is True
    assert execution.music.intensity is Intensity.HIGH
    assert execution.music.palette is MusicPalette.MELANCHOLIC_ENERGETIC
    assert execution.preset is None


def test_hue_from_dict_builds_groups_with_ids():
    hue = HueData.from_dict(_data()["hue"])

    assert hue.bridge_unique_id == "001788FFFE000000"
    assert hue.connection_state is ConnectionState.CONNECTED
    assert set(hue.groups.keys()) == {
        "db7dd240-d061-48bf-84c2-01f086e4bfae",
        "f7bd7dcb-bbcb-4cd1-b343-126e60575884",
    }

    group = hue.groups["db7dd240-d061-48bf-84c2-01f086e4bfae"]
    assert group.id == "db7dd240-d061-48bf-84c2-01f086e4bfae"
    assert group.name == "TV Area"
    assert group.num_lights == 5
    assert group.active is False
    assert group.owner is None


def test_execution_mode_preserves_values_added_by_new_firmware():
    raw = _data()["execution"]
    raw["mode"] = "futureMode"

    execution = ExecutionData.from_dict(raw)

    assert execution.mode.value == "futureMode"
    assert execution.to_dict()["mode"] == "futureMode"


def test_hdmi_and_behavior_parse_protocol_enums():
    hdmi = HdmiData.from_dict(
        {
            "contentSpecs": "3840 x 2160 @ 60000 - SDR",
            "videoSyncSupported": True,
            "audioSyncSupported": True,
            "input1": {
                "name": "HDMI 1",
                "type": "xbox",
                "status": "plugged",
                "lastSyncMode": "game",
            },
            "input2": {
                "name": "HDMI 2",
                "type": "generic",
                "status": "unplugged",
                "lastSyncMode": "video",
            },
            "input3": {
                "name": "HDMI 3",
                "type": "generic",
                "status": "unplugged",
                "lastSyncMode": "video",
            },
            "input4": {
                "name": "HDMI 4",
                "type": "generic",
                "status": "unplugged",
                "lastSyncMode": "video",
            },
            "output": {
                "name": "HDMI Out",
                "type": "generic",
                "status": "linked",
                "lastSyncMode": "video",
            },
        }
    )
    behavior = BehaviorData.from_dict(
        {
            "inactivePowersave": 20,
            "cecPowersave": 1,
            "usbPowersave": 1,
            "hpdInputSwitch": 0,
        }
    )

    assert hdmi.input1.type is PortType.XBOX
    assert hdmi.output.status is PortStatus.LINKED
    assert behavior.cec_powersave is True
    assert behavior.hpd_input_switch is False


def test_registration_role_parses_as_enum():
    registration = Registration.from_dict(
        {
            "appName": "Hue Sync Android",
            "instanceName": "Pixel",
            "role": "admin",
            "lastUsed": "2020-02-16T05:45:20Z",
            "created": "2020-01-11T05:45:20Z",
        }
    )

    assert registration.role is RegistrationRole.ADMIN


def test_update_models_serialize_partial_camel_case_payloads():
    execution = ExecutionUpdate(
        sync_active=True,
        hdmi_source=HdmiSource.INPUT2,
        brightness=None,
    )
    hue = HueUpdate(bridge_unique_id="001788FFFE000000", username="user")

    assert execution.to_dict() == {"syncActive": True, "hdmiSource": "input2"}
    assert hue.to_dict() == {
        "bridgeUniqueId": "001788FFFE000000",
        "username": "user",
    }
