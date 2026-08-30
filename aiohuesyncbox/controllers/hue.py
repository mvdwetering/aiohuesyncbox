from typing import TYPE_CHECKING

from ..models import Group, GroupUpdate, HueData, HueUpdate, RequestFunc
from ..models.enums import ConnectionState
from .base import Resource


class Hue(Resource[HueData]):
    """Control the Hue resource of the huesyncbox."""

    if TYPE_CHECKING:
        # __getattr__ delegates these to self._data at runtime; declared here
        # only so type checkers see real types instead of Any.
        bridge_unique_id: str
        bridge_ip_address: str
        connection_state: ConnectionState

    def __init__(self, data: HueData, request: RequestFunc) -> None:
        super().__init__("/hue", data, request)

    @property
    def groups(self) -> list[Group]:
        """Available entertainment areas."""
        return list(self._data.groups.values())

    @property
    def groups_by_id(self) -> dict[str, Group]:
        """Available entertainment areas keyed by API id."""
        return self._data.groups

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
