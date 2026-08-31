from typing import TYPE_CHECKING, Any

from ..models import IrCode, IrCodeUpdate, IrData, RequestFunc, ScanState, ScanUpdate
from .base import Resource


class Ir(Resource[IrData]):
    """Control the IR resource of the huesyncbox."""

    if TYPE_CHECKING:
        # __getattr__ delegates these to self._data at runtime; declared here
        # so type checkers see real types instead of Any.
        default_codes: bool
        scan: ScanState
        codes: dict[str, IrCode]

    def __init__(self, data: IrData, request: RequestFunc) -> None:
        super().__init__("/ir", data, request)

    async def set_scanning(self, scanning: bool) -> None:
        """Enable/disable IR code scanning mode."""
        await self._request("put", "/ir/scan", data=ScanUpdate(scanning=scanning).to_dict())

    async def set_code(
        self, code: str, name: str, execution: dict[str, Any]
    ) -> None:
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
