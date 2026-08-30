from dataclasses import dataclass

from .base import BaseModel, UpdateModel
from .enums import PortStatus, PortType, SyncMode

INPUTS = ["input1", "input2", "input3", "input4"]


@dataclass
class Port(BaseModel):
    """Represent an HDMI input or output port."""

    name: str
    """User-assigned port name."""
    type: PortType
    """User-assigned device type for the port."""
    status: PortStatus
    last_sync_mode: SyncMode
    """Most recently used sync mode for this port."""


@dataclass
class Input(Port):
    pass


@dataclass
class Output(Port):
    pass


@dataclass
class PortUpdate(UpdateModel):
    """Mutable name and type fields for an HDMI port."""

    name: str | None = None
    type: PortType | None = None


@dataclass
class HdmiData(BaseModel):
    """State returned by the `/hdmi` endpoint."""

    content_specs: str
    """Current video resolution, frame rate, and HDR format."""
    video_sync_supported: bool
    """Whether current content can be synchronized in video or game mode."""
    audio_sync_supported: bool
    """Whether current content can be synchronized in music mode."""
    output: Output
    input1: Input
    input2: Input
    input3: Input
    input4: Input
