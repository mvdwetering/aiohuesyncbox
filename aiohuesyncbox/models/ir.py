from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base import BaseModel


@dataclass
class ScanState(BaseModel):
    """State of IR code scanning."""

    scanning: bool
    #: Last scanned code received while in scanning mode, null if none scanned yet.
    code: Optional[str] = None
    codes: List[str] = field(default_factory=list)


@dataclass
class IrCode(BaseModel):
    """A single configured IR code."""

    name: str
    #: Execution object with only a single key-value pair to apply when the code is received.
    execution: Dict[str, Any] = field(default_factory=dict)

    #: Not part of the JSON body, it is the dict key under `IrData.codes`.
    code: str = field(default="", compare=False, metadata={"serialize": "omit"})


@dataclass
class IrData(BaseModel):
    """Represent IR config of huesyncbox."""

    default_codes: bool
    scan: ScanState
    codes: Dict[str, IrCode] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for code, ir_code in self.codes.items():
            ir_code.code = code
