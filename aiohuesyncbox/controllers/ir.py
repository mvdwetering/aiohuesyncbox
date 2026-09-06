from typing import Any

from ..models import IrCode, IrCodeUpdate, IrData, RequestFunc, ScanState, ScanUpdate
from .base import Resource


class Ir(Resource[IrData]):
    """Control the IR resource of the huesyncbox."""

    def __init__(self, data: IrData, request: RequestFunc) -> None:
        super().__init__("/ir", data, request)

    @property
    def default_codes(self) -> bool:
        return self._data.default_codes

    @property
    def scan(self) -> ScanState:
        return self._data.scan

    @property
    def codes(self) -> dict[str, IrCode]:
        return self._data.codes

    async def set_scanning(self, scanning: bool) -> None:
        """Enable/disable IR code scanning mode."""
        await self._request(
            "put", "/ir/scan", data=ScanUpdate(scanning=scanning).to_dict()
        )

    async def set_code(self, code: str, name: str, execution: dict[str, Any]) -> None:
        """Create or update an IR code mapping."""
        await self._request(
            "put",
            f"/ir/codes/{code}",
            data=IrCodeUpdate(name=name, execution=execution).to_dict(),
        )

    async def delete_code(self, code: str) -> None:
        await self._request("delete", f"/ir/codes/{code}")

    def get_code(self, code: str) -> IrCode | None:
        return self._data.codes.get(code)
