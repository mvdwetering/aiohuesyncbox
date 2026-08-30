from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseModel, UpdateModel


@dataclass
class ScanState(BaseModel):
    """IR scan state; scanning stops after the next received code or 20 seconds."""

    scanning: bool
    code: Optional[str] = None
    codes: List[str] = field(default_factory=list)


@dataclass
class ScanUpdate(UpdateModel):
    """Partial change accepted by the `/ir/scan` endpoint."""

    scanning: bool | None = None


@dataclass
class IrCode(BaseModel):
    """Configured IR code with one execution action."""

    name: str
    execution: Dict[str, Any] = field(default_factory=dict)
    code: str = field(default="", compare=False, metadata={"serialize": "omit"})


@dataclass
class IrCodeUpdate(UpdateModel):
    """Mutable fields accepted by an individual `/ir/codes/{code}` endpoint."""

    name: str | None = None
    execution: Dict[str, Any] | None = None


@dataclass
class IrData(BaseModel):
    """State returned by the `/ir` endpoint; codes are keyed by their hex value."""

    default_codes: bool
    scan: ScanState
    codes: Dict[str, IrCode] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for code, ir_code in self.codes.items():
            ir_code.code = code
