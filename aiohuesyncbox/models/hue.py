from dataclasses import dataclass, field
from typing import Dict, Optional

from .base import BaseModel
from .enums import ConnectionState


@dataclass
class Group(BaseModel):
    """Represent a group (entertainment area) on the Hue bridge"""

    name: str
    num_lights: int
    active: bool
    #: User friendly name of the application that is streaming on the
    #: associated bridge. Only exposed if active is true.
    owner: Optional[str] = None

    #: Not part of the JSON body, it is the dict key under `HueData.groups`.
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})


@dataclass
class HueData(BaseModel):
    """Represent Hue config."""

    bridge_unique_id: str
    bridge_ip_address: str
    #: uninitialized, disconnected, connecting, unauthorized, connected, invalidgroup, streaming
    connection_state: ConnectionState
    #: All available entertainment areas on the current bridge, keyed by id.
    #: When this object is not available, it means the bridge groups have not
    #: been retrieved yet. When empty, there are no entertainment areas on the
    #: bridge. When the bridge connection is lost, the last known values are
    #: remembered; use connection_state to determine if they may be outdated.
    groups: Dict[str, Group] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for group_id, group in self.groups.items():
            group.id = group_id
