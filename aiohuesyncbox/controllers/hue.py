from ..models import GroupUpdate, HueData, HueUpdate, RequestFunc
from .base import Resource


class Hue(Resource[HueData]):
    """Control the Hue resource of the huesyncbox."""

    def __init__(self, data: HueData, request: RequestFunc) -> None:
        super().__init__("/hue", data, request)

    async def set_group_active(self, id: str, active: bool) -> None:
        await self._request(
            "put", f"/hue/groups/{id}", data=GroupUpdate(active=active).to_dict()
        )

    async def set_bridge(
        self,
        bridge_unique_id: str,
        username: str,
        client_key: str,
    ) -> None:
        """Change bridge used by huesyncbox."""
        update = HueUpdate(
            bridge_unique_id=bridge_unique_id,
            username=username,
            client_key=client_key,
        )
        await self._put(update.to_dict())
