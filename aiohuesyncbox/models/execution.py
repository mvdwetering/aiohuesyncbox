from dataclasses import dataclass
from typing import Optional

from .base import BaseModel, UpdateModel
from .enums import CycleDirection, ExecutionMode, HdmiSource, Intensity, MusicPalette, SyncMode


@dataclass
class VideoMode(BaseModel):
    """Video (or game) mode execution state."""

    intensity: Intensity
    background_lighting: bool


@dataclass
class GameMode(VideoMode):
    pass


@dataclass
class MusicMode(BaseModel):
    """Music mode execution state."""

    intensity: Intensity
    palette: MusicPalette


@dataclass
class ExecutionUpdate(UpdateModel):
    """Partial state change accepted by the `/execution` endpoint."""

    sync_active: Optional[bool] = None
    toggle_sync_active: Optional[bool] = None
    hdmi_active: Optional[bool] = None
    toggle_hdmi_active: Optional[bool] = None
    mode: Optional[ExecutionMode] = None
    cycle_sync_mode: Optional[CycleDirection] = None
    hdmi_source: Optional[HdmiSource] = None
    cycle_hdmi_source: Optional[CycleDirection] = None
    brightness: Optional[int] = None
    increment_brightness: Optional[int] = None
    intensity: Optional[Intensity] = None
    cycle_intensity: Optional[CycleDirection] = None
    video: Optional[VideoMode] = None
    game: Optional[GameMode] = None
    music: Optional[MusicMode] = None
    hue_target: Optional[str] = None


@dataclass
class ExecutionData(BaseModel):
    """State returned by the `/execution` endpoint."""

    sync_active: bool
    """False in powersave/passthrough; true while syncing in a sync mode."""
    hdmi_active: bool
    """False in powersave; true while passing through or syncing HDMI content."""
    mode: ExecutionMode
    last_sync_mode: SyncMode
    """Most recently used sync mode."""
    hdmi_source: HdmiSource
    """Currently selected HDMI input."""
    hue_target: str
    """Entertainment-area identifier, either `groups/<id>` or an entertainmentconfiguration UUID."""
    brightness: int
    """0 - 200 (100 = no brightness reduction/boost compared to input, 0 = max reduction, 200 = max boost)."""
    video: VideoMode
    game: GameMode
    music: MusicMode
    preset: Optional[str] = None
    """Identifier of the preset currently being executed, when one is active."""
