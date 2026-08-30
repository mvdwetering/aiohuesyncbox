from typing import Any, Dict, Optional

from ..models import IrCode, IrData, RequestFunc
from .base import Resource


class Ir(Resource[IrData]):
    """Control the IR resource of the huesyncbox."""

    def __init__(self, data: IrData, request: RequestFunc) -> None:
        super().__init__("/ir", data, request)

    async def set_scanning(self, scanning: bool) -> None:
        """Enable/disable IR code scanning mode."""
        await self._request("put", "/ir/scan", data={"scanning": scanning})

    async def set_code(
        self, code: str, name: str, execution: Dict[str, Any]
    ) -> None:
        """Create or update an IR code mapping."""
        await self._request(
            "put",
            f"/ir/codes/{code}",
            data={"name": name, "execution": execution},
        )

    async def delete_code(self, code: str) -> None:
        await self._request("delete", f"/ir/codes/{code}")

    def get_code(self, code: str) -> Optional[IrCode]:
        return self._data.codes.get(code)
