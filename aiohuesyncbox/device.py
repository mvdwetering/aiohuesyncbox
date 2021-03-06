from .helpers import generate_attribute_string


class Device:
    """Represent Device config."""

    def __init__(self, raw, request) -> None:
        self._raw = raw
        self._request = request

    def __str__(self) -> str:
        attributes = [
            "name",
            "device_type",
            "unique_id",
            "ip_address",
            "api_level",
            "firmware_version",
        ]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        return self._raw == other._raw

    @property
    def name(self) -> str:
        """Friendly name of the device."""
        return self._raw["name"]

    @property
    def device_type(self) -> str:
        """Device Type identifier."""
        return self._raw["deviceType"]

    @property
    def unique_id(self) -> str:
        """Capitalized hex string of the 6 byte / 12 characters device id without delimiters. Used as unique id on label, certificate common name, hostname etc."""
        return self._raw["uniqueId"]

    @property
    def ip_address(self) -> str:
        """Local IP address of the device."""
        return self._raw["ipAddress"]

    @property
    def api_level(self) -> int:
        """Supported API level of the device."""
        return self._raw["apiLevel"]

    @property
    def firmware_version(self) -> str:
        """User readable version of the device firmware, starting with decimal major .minor .maintenance format e.g. 1.12.3."""
        return self._raw["firmwareVersion"]

    async def update(self) -> None:
        response = await self._request("get", "/device")
        if response:
            self._raw = response