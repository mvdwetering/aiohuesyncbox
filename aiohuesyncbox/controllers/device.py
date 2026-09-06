from ..models import (
    DeviceAutoUpdate,
    DeviceCapabilities,
    DeviceData,
    DeviceUpdate,
    RequestFunc,
    Wifi,
)
from ..models.enums import DeviceAction, LedMode, WifiState
from .base import Resource


class Device(Resource[DeviceData]):
    """Control the Device resource of the huesyncbox."""

    def __init__(self, data: DeviceData, request: RequestFunc) -> None:
        super().__init__("/device", data, request)

    @property
    def name(self) -> str:
        return self._data.name

    @property
    def device_type(self) -> str:
        return self._data.device_type

    @property
    def unique_id(self) -> str:
        return self._data.unique_id

    @property
    def ip_address(self) -> str:
        return self._data.ip_address

    @property
    def api_level(self) -> int:
        return self._data.api_level

    @property
    def firmware_version(self) -> str:
        return self._data.firmware_version

    @property
    def build_number(self) -> int:
        return self._data.build_number

    @property
    def led_mode(self) -> LedMode:
        return self._data.led_mode

    @property
    def wifi(self) -> Wifi | None:
        return self._data.wifi

    @property
    def wifi_state(self) -> WifiState | None:
        return self._data.wifi_state

    @property
    def updatable_firmware_version(self) -> str | None:
        return self._data.updatable_firmware_version

    @property
    def updatable_build_number(self) -> int | None:
        return self._data.updatable_build_number

    @property
    def last_checked_update(self) -> str | None:
        return self._data.last_checked_update

    @property
    def update(self) -> DeviceAutoUpdate | None:
        return self._data.update

    @property
    def action(self) -> DeviceAction | None:
        return self._data.action

    @property
    def pushlink(self) -> str | None:
        return self._data.pushlink

    @property
    def overheating(self) -> bool | None:
        return self._data.overheating

    @property
    def undervolt(self) -> bool | None:
        return self._data.undervolt

    @property
    def bluetooth(self) -> bool | None:
        return self._data.bluetooth

    @property
    def capabilities(self) -> DeviceCapabilities | None:
        return self._data.capabilities

    async def set_led_mode(self, mode: LedMode) -> None:
        await self._put(DeviceUpdate(led_mode=mode).to_dict())
