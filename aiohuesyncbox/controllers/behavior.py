from typing import TYPE_CHECKING

from ..models import BehaviorData, BehaviorUpdate, InputBehavior, RequestFunc
from ..models.enums import Enabled
from .base import Resource


class Behavior(Resource[BehaviorData]):
    """Control the Behavior resource of the huesyncbox."""

    if TYPE_CHECKING:
        # __getattr__ delegates these to self._data at runtime; declared here
        # so type checkers see real types instead of Any.
        inactive_powersave: int
        cec_powersave: Enabled
        usb_powersave: Enabled | None
        hpd_input_switch: Enabled | None
        force_dovi_native: Enabled | None
        input1: InputBehavior | None
        input2: InputBehavior | None
        input3: InputBehavior | None
        input4: InputBehavior | None

    def __init__(self, data: BehaviorData, request: RequestFunc) -> None:
        super().__init__("/behavior", data, request)

    async def set_force_dovi_native(self, enabled: bool) -> None:
        """Force DolbyVision compatibility of huesyncbox on or off."""
        mode = Enabled.ENABLED if enabled else Enabled.DISABLED
        await self._put(BehaviorUpdate(force_dovi_native=mode).to_dict())
