from typing import Any, Dict, Optional

from ..models import Preset, RequestFunc
from .base import CollectionResource


class Presets(CollectionResource[Preset]):
    """Control the Presets resource of the huesyncbox."""

    def __init__(self, request: RequestFunc) -> None:
        super().__init__("/presets", Preset, request)

    async def create(self, name: str, execution: Dict[str, Any]) -> Optional[str]:
        """Create a new preset, returns the generated preset id."""
        response = await self._request(
            "post", self._path, {"name": name, "execution": execution}
        )
        return response.get("id") if response else None

    async def set(
        self,
        id: str,
        name: Optional[str] = None,
        execution: Optional[Dict[str, Any]] = None,
    ) -> None:
        data = {
            key: value
            for key, value in {"name": name, "execution": execution}.items()
            if value is not None
        }
        await self._request("put", f"{self._path}/{id}", data=data)
