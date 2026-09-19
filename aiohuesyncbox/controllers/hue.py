from ..models import (
    BleConnectionState,
    BleEntertainmentLightItem,
    Group,
    GroupUpdate,
    HueData,
    HueUpdate,
    RequestFunc,
)
from ..models.enums import ConnectionState, OperatingMode
from .base import Resource


class Hue(Resource[HueData]):
    """Control the Hue resource of the huesyncbox."""

    def __init__(self, data: HueData, request: RequestFunc) -> None:
        super().__init__("/hue", data, request)

    @property
    def bridge_unique_id(self) -> str | None:
        return self._data.bridge_unique_id

    @property
    def bridge_ip_address(self) -> str | None:
        return self._data.bridge_ip_address

    @property
    def connection_state(self) -> ConnectionState:
        return self._data.connection_state

    @property
    def operating_mode(self) -> OperatingMode | None:
        return self._data.operating_mode

    @property
    def group_id(self) -> str | None:
        return self._data.group_id

    @property
    def ble_connection_state(self) -> BleConnectionState | None:
        return self._data.ble_connection_state

    @property
    def ble_entertainment_lights(self) -> list[BleEntertainmentLightItem]:
        return self._data.ble_entertainment_lights

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

    async def set_group_id(self, group_id: str) -> None:
        """Select entertainment area."""
        await self._put(HueUpdate(group_id=group_id).to_dict())

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
