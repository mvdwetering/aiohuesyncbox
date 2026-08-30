from ..models import HueData, RequestFunc
from .base import Resource


class Hue(Resource[HueData]):
    """Control the Hue resource of the huesyncbox."""

    def __init__(self, data: HueData, request: RequestFunc) -> None:
        super().__init__("/hue", data, request)

    async def set_group_active(self, id: str, active: bool) -> None:
        await self._request("put", f"/hue/groups/{id}", data={"active": active})

    async def set_bridge(
        self,
        bridge_unique_id: str,
        username: str,
        client_key: str,
    ) -> None:
        """Change bridge used by huesyncbox."""
        await self._put(
            {
                "bridgeUniqueId": bridge_unique_id,
                "username": username,
                "clientKey": client_key,
            }
        )
