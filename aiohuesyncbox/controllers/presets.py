from typing import Any

from ..models import Preset, PresetCreate, PresetUpdate, RequestFunc
from .base import CollectionResource


class Presets(CollectionResource[Preset]):
    """Control the Presets resource of the huesyncbox."""

    def __init__(self, request: RequestFunc) -> None:
        super().__init__("/presets", Preset, request)

    async def create(self, name: str, execution: dict[str, Any]) -> str | None:
        """Create a new preset, returns the generated preset id."""
        response = await self._request(
            "post", self._path, PresetCreate(name=name, execution=execution).to_dict()
        )
        return response.get("id") if response else None

    async def set(
        self,
        id: str,
        name: str | None = None,
        execution: dict[str, Any] | None = None,
    ) -> None:
        update = PresetUpdate(name=name, execution=execution)
        await self._request("put", f"{self._path}/{id}", data=update.to_dict())
