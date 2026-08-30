from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .base import BaseModel, UpdateModel


@dataclass
class Preset(BaseModel):
    """Stored execution preset."""

    name: str
    """User-assigned preset name, limited to 24 bytes by the Sync Box."""
    last_used: Optional[str] = None
    """UTC ISO 8601 timestamp at which the preset was last activated."""
    execution: Dict[str, Any] = field(default_factory=dict)
    """Execution change applied on activation; may not reference another preset."""
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})
    """Preset id derived from the containing presets map key."""


@dataclass
class PresetCreate(BaseModel):
    """Payload accepted by `POST /presets`."""

    name: str
    execution: Dict[str, Any]


@dataclass
class PresetUpdate(UpdateModel):
    """Partial change accepted by an individual preset endpoint."""

    name: str | None = None
    execution: Dict[str, Any] | None = None
