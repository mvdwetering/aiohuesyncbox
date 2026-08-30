from typing import TYPE_CHECKING

from ..models import DeviceAutoUpdate, DeviceCapabilities, DeviceData, DeviceUpdate, RequestFunc, Wifi
from ..models.enums import DeviceAction, LedMode, WifiState
from .base import Resource


class Device(Resource[DeviceData]):
    """Control the Device resource of the huesyncbox."""

    if TYPE_CHECKING:
        # __getattr__ delegates these to self._data at runtime; declared here
        # only so type checkers see real types instead of Any.
        name: str
        device_type: str
        unique_id: str
        ip_address: str
        api_level: int
        firmware_version: str
        build_number: int
        led_mode: LedMode
        wifi: Wifi | None
        wifi_state: WifiState | None
        updatable_firmware_version: str | None
        updatable_build_number: int | None
        last_checked_update: str | None
        update: DeviceAutoUpdate | None
        action: DeviceAction | None
        pushlink: str | None
        overheating: bool | None
        undervolt: bool | None
        bluetooth: bool | None
        capabilities: DeviceCapabilities | None

    def __init__(self, data: DeviceData, request: RequestFunc) -> None:
        super().__init__("/device", data, request)

    async def set_led_mode(self, mode: LedMode) -> None:
        await self._put(DeviceUpdate(led_mode=mode).to_dict())
