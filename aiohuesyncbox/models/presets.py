from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .base import BaseModel


@dataclass
class Preset(BaseModel):
    """Represent a single preset."""

    name: str
    #: UTC time when this preset was last used.
    last_used: Optional[str] = None
    #: Object to write to execution when preset is activated. May not contain the "preset" key itself.
    execution: Dict[str, Any] = field(default_factory=dict)

    #: Not part of the JSON body, it is the dict key under the presets map.
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})
