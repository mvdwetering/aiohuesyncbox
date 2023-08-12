from .helpers import generate_attribute_string


class Wifi:
    """Represent wifi status"""

    def __init__(self, raw) -> None:
        self._raw = raw

    @property
    def ssid(self) -> str:
        """Wifi SSID"""
        return self._raw["ssid"]

    @property
    def strength(self) -> int:
        """
        0 = not connected; 1 = weak; 2 = fair; 3 = good; 4 = excellent
        """
        return self._raw["strength"]


class Device:
    """Represent Device config."""

    def __init__(self, raw, request) -> None:
        self._raw = raw
        self._request = request
        self._wifi = Wifi(self._raw["wifi"])

    def __str__(self) -> str:
        attributes = [
            "name",
            "device_type",
            "unique_id",
            "ip_address",
            "api_level",
            "firmware_version",
            "wifi",
        ]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Device):
            return NotImplemented
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

    @property
    def wifi(self) -> Wifi | None:
        """Root object for Wifi information if available."""
        return self._wifi

    @property
    def led_mode(self) -> int:
        """
        0 = off in powersave, passthrough or sync mode; 1 = regular; 2 = dimmed in powersave or passthrough mode and off in sync mode
        """
        return self._raw["ledMode"]

    async def set_led_mode(self, mode: int) -> None:
        await self._request("put", f"/device", data={"ledMode": mode})

    async def update(self) -> None:
        response = await self._request("get", "/device")
        if response:
            self._raw = response
            self._wifi = Wifi(self._raw["wifi"]) if "wifi" in self._raw else None
