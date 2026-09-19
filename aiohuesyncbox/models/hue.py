from dataclasses import dataclass, field

from .base import BaseModel, UpdateModel
from .enums import ConnectionState, OperatingMode


@dataclass
class BleConnectionState(BaseModel):
    """BLE connection state for standalone entertainment mode (HSB2/HSB3/HSC1 only)."""

    state: str | None = None


@dataclass
class BleLightRead(BaseModel):
    """BLE light properties returned in GET responses."""

    ble_dlc_key: str | None = None
    zigbee_mac_address: str | None = None


@dataclass
class BleLightWrite(BaseModel):
    """BLE light properties accepted in PUT requests."""

    ble_dlc_key: str
    zigbee_mac_address: str


@dataclass
class BleEntertainmentLightItem(BaseModel):
    """A BLE entertainment light entry (read response)."""

    light: BleLightRead | None = None


@dataclass
class BleEntertainmentLightItemWrite(BaseModel):
    """A BLE entertainment light entry (write request)."""

    light: BleLightWrite


@dataclass
class Group(BaseModel):
    """Hue entertainment area."""

    name: str
    """Friendly name of the entertainment area."""
    num_lights: int
    """Number of lights in the entertainment area."""
    active: bool
    """Whether streaming is currently active on this area."""
    owner: str | None = None
    """Only exposed if active is true."""
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})
    """API group id derived from the containing `groups` map key."""


@dataclass
class GroupUpdate(UpdateModel):
    """Mutable fields accepted by an individual Hue group endpoint."""

    active: bool | None = None
    """Whether streaming is currently active on this area."""


@dataclass
class HueUpdate(UpdateModel):
    """Bridge pairing and configuration fields accepted by the `/hue` endpoint."""

    bridge_unique_id: str | None = None
    """Unique id of the connected bridge."""
    username: str | None = None
    """randomly-generated username for Hue bridge, also referred to as application_key or hue-application-key."""
    client_key: str | None = None
    """32 character ASCII hex representation of 16 byte client key needed for streaming to hue entertainment."""
    group_id: str | None = None
    """Id of the currently selected entertainment area. Added in API level 10."""


@dataclass
class HueData(BaseModel):
    """State returned by the `/hue` endpoint."""

    connection_state: ConnectionState
    bridge_unique_id: str | None = None
    """Unique id of the connected bridge."""
    bridge_ip_address: str | None = None
    """Local IP address of the device."""
    operating_mode: OperatingMode | None = None
    """Derived operating mode based on stored configuration. HSB2/HSB3/HSC1 only. Added in API level 14."""
    group_id: str | None = None
    """Id of the currently selected entertainment area. Added in API level 10."""
    ble_connection_state: BleConnectionState | None = None
    """BLE connection state object. HSB2/HSB3/HSC1 only. Added in API level 14."""
    ble_entertainment_lights: list[BleEntertainmentLightItem] = field(
        default_factory=list
    )
    """Array of provisioned BLE entertainment lights. HSB2/HSB3/HSC1 only. Added in API level 14."""
    groups: dict[str, Group] = field(default_factory=dict)
    """Entertainment areas keyed by API id."""

    def __post_init__(self) -> None:
        for group_id, group in self.groups.items():
            group.id = group_id
