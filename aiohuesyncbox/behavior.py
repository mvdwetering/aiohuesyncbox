from typing import Dict
from .helpers import generate_attribute_string


class Behavior:
    """Represent Behavior config of huesyncbox."""

    def __init__(self, raw, request) -> None:
        self._raw = raw
        self._request = request

    async def _put(self, data: Dict) -> None:
        await self._request("put", "/behavior", data=data)

    def __str__(self):
        attributes = [
            "forceDoviNative",
        ]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Behavior):
            return NotImplemented
        return self._raw == other._raw

    @property
    def force_dovi_native(self) -> int | None:
        """When the TV advertises Dolby Vision force to use native native mode. Disabled 0, Enabled 1."""
        return self._raw.get("forceDoviNative")

    async def set_force_dovi_native(self, enabled: int) -> None:
        """Force DolbyVision compatibility of huesyncbox on or off."""
        data = {"forceDoviNative": enabled}
        await self._put(data)

    async def update(self) -> None:
        response = await self._request("get", "/behavior")
        if response:
            self._raw = response
