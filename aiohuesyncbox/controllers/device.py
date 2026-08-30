from ..models import DeviceData, DeviceUpdate, RequestFunc
from ..models.enums import LedMode
from .base import Resource


class Device(Resource[DeviceData]):
    """Control the Device resource of the huesyncbox."""

    def __init__(self, data: DeviceData, request: RequestFunc) -> None:
        super().__init__("/device", data, request)

    async def set_led_mode(self, mode: LedMode) -> None:
        await self._put(DeviceUpdate(led_mode=mode).to_dict())
