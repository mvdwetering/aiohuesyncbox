from ..models import BehaviorData, RequestFunc
from ..models.enums import Enabled
from .base import Resource


class Behavior(Resource[BehaviorData]):
    """Control the Behavior resource of the huesyncbox."""

    def __init__(self, data: BehaviorData, request: RequestFunc) -> None:
        super().__init__("/behavior", data, request)

    async def set_force_dovi_native(self, enabled: Enabled) -> None:
        """Force DolbyVision compatibility of huesyncbox on or off."""
        await self._put({"forceDoviNative": enabled})
