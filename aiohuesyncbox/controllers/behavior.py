from ..models import BehaviorData, BehaviorUpdate, InputBehavior, RequestFunc
from .base import Resource


class Behavior(Resource[BehaviorData]):
    """Control the Behavior resource of the huesyncbox."""

    def __init__(self, data: BehaviorData, request: RequestFunc) -> None:
        super().__init__("/behavior", data, request)

    @property
    def inactive_powersave(self) -> int:
        return self._data.inactive_powersave

    @property
    def cec_powersave(self) -> bool:
        return self._data.cec_powersave

    @property
    def usb_powersave(self) -> bool | None:
        return self._data.usb_powersave

    @property
    def hpd_input_switch(self) -> bool | None:
        return self._data.hpd_input_switch

    @property
    def force_dovi_native(self) -> bool | None:
        return self._data.force_dovi_native

    @property
    def input1(self) -> InputBehavior | None:
        return self._data.input1

    @property
    def input2(self) -> InputBehavior | None:
        return self._data.input2

    @property
    def input3(self) -> InputBehavior | None:
        return self._data.input3

    @property
    def input4(self) -> InputBehavior | None:
        return self._data.input4

    async def set_force_dovi_native(self, enabled: bool) -> None:
        """Force DolbyVision compatibility of huesyncbox on or off."""
        await self._put(BehaviorUpdate(force_dovi_native=enabled).to_dict())
