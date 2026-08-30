from ..models import BehaviorData, BehaviorUpdate, RequestFunc
from ..models.enums import Enabled
from .base import Resource


class Behavior(Resource[BehaviorData]):
    """Control the Behavior resource of the huesyncbox."""

    def __init__(self, data: BehaviorData, request: RequestFunc) -> None:
        super().__init__("/behavior", data, request)

    async def set_force_dovi_native(self, enabled: bool) -> None:
        """Force DolbyVision compatibility of huesyncbox on or off."""
        mode = Enabled.ENABLED if enabled else Enabled.DISABLED
        await self._put(BehaviorUpdate(force_dovi_native=mode).to_dict())
