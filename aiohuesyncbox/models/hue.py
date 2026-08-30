from dataclasses import dataclass, field

from .base import BaseModel, UpdateModel
from .enums import ConnectionState


@dataclass
class Group(BaseModel):
    """Hue entertainment area."""

    name: str
    """User-assigned entertainment area name."""
    num_lights: int
    """Number of lights in the entertainment area."""
    active: bool
    """Whether this area is being streamed by the Sync Box or another source."""
    owner: str | None = None
    """Streaming application name, populated only while the group is active."""
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})
    """API group id derived from the containing `groups` map key."""


@dataclass
class GroupUpdate(UpdateModel):
    """Mutable fields accepted by an individual Hue group endpoint."""

    active: bool | None = None
    """Whether to enable streaming for this entertainment area."""


@dataclass
class HueUpdate(UpdateModel):
    """Bridge pairing fields accepted by the `/hue` endpoint."""

    bridge_unique_id: str | None = None
    """16-character hexadecimal identifier of the paired Hue bridge."""
    username: str | None = None
    """Hue bridge application key, also known as a Hue username."""
    client_key: str | None = None
    """32-character hexadecimal client key used for Hue entertainment streaming."""


@dataclass
class HueData(BaseModel):
    """State returned by the `/hue` endpoint."""

    bridge_unique_id: str
    """16-character hexadecimal identifier of the paired Hue bridge."""
    bridge_ip_address: str
    """IPv4 address of the paired Hue bridge."""
    connection_state: ConnectionState
    """Current connection state between the Sync Box and the Hue bridge."""
    groups: dict[str, Group] = field(default_factory=dict)
    """Entertainment areas keyed by API id.

    The Sync Box omits this field until areas are first retrieved. On a lost
    bridge connection it retains the last known areas; use `connection_state`
    to determine whether these values may be stale.
    """

    def __post_init__(self) -> None:
        for group_id, group in self.groups.items():
            group.id = group_id
