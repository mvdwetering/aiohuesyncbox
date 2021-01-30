from .helpers import generate_attribute_string

class Group:
    """Represent a group on the Hue bridge"""

    def __init__(self, id, raw):
        self._id = id
        self._raw = raw

    @property
    def id(self):
        """Id of the group."""
        return self._id

    @property
    def name(self):
        """Friendly name of the entertainment group."""
        return self._raw['name']

    @property
    def num_lights(self):
        """Number of lights in the entertainment group."""
        return self._raw['numLights']

    @property
    def active(self):
        """Indicates if the group is actively streaming (either from Syncbox or other source)."""
        return self._raw['active']

    @property
    def owner(self):
        """
        User friendly name of the application that is streaming on the associated bridge.
        Only exposed if active is true
        """
        return self._raw['owner'] if 'owner' in self._raw else None


class Hue:
    """Represent Hue config."""

    def __init__(self, raw, request):
        self._raw = raw
        self._request = request
        self._groups = Hue._build_groups(self._raw)

    def __str__(self):
        attributes = ["bridge_unique_id", "bridge_ip_address", "connection_state", "groups"]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        return self._raw == other._raw

    @staticmethod
    def _build_groups(raw):
        groups = []
        for key, value in raw['groups'].items():
            groups.append(Group(key, value))
        return groups

    @property
    def bridge_unique_id(self):
        """16 character ascii hex string bridge identifier."""
        return self._raw['bridgeUniqueId']

    @property
    def bridge_ip_address(self):
        """Readable, dot IPv4 address of the paired bridge EG 192.168.1.50."""
        return self._raw['bridgeIpAddress']

    @property
    def connection_state(self):
        """uninitialized, disconnected, connecting, unauthorized, connected, invalidgroup, streaming"""
        return self._raw['connectionState']

    @property
    def groups(self):
        """
        All available entertainment areas on the current bridge.
        When this object is not available, it means the bridge groups have not been retrieved yet.
        When the object is empty, it means there are no entertainment areas on the bridge.
        When the bridge connection is lost, the last known values are remembered.
        Determining whether values may be outdated can be done based on connectionState.
        """
        return self._groups

    async def set_group_active(self, id, active):
        data = { 'active': active }
        await self._request('put', f'/hue/groups/{id}', data=data)

    async def update(self):
        response = await self._request('get', '/hue')
        if response:
            self._raw = response
            self._groups = Hue._build_groups(self._raw)
