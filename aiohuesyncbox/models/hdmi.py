from dataclasses import dataclass

from .base import BaseModel
from .enums import PortStatus, PortType, SyncMode

INPUTS = ["input1", "input2", "input3", "input4"]


@dataclass
class Port(BaseModel):
    """Represent an HDMI input or output port."""

    name: str
    type: PortType
    #: unplugged, plugged, linked, unknown
    status: PortStatus
    last_sync_mode: SyncMode


@dataclass
class Input(Port):
    pass


@dataclass
class Output(Port):
    pass


@dataclass
class HdmiData(BaseModel):
    """Represent Hdmi config of huesyncbox."""

    content_specs: str
    video_sync_supported: bool
    audio_sync_supported: bool
    output: Output
    input1: Input
    input2: Input
    input3: Input
    input4: Input
