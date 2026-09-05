from dataclasses import dataclass

from .base import BaseModel, UpdateModel
from .enums import (
    CycleDirection,
    ExecutionMode,
    HdmiSource,
    Intensity,
    MusicPalette,
    SyncMode,
)


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

    sync_active: bool | None = None
    toggle_sync_active: bool | None = None
    hdmi_active: bool | None = None
    toggle_hdmi_active: bool | None = None
    mode: ExecutionMode | None = None
    cycle_sync_mode: CycleDirection | None = None
    hdmi_source: HdmiSource | None = None
    cycle_hdmi_source: CycleDirection | None = None
    brightness: int | None = None
    increment_brightness: int | None = None
    intensity: Intensity | None = None
    cycle_intensity: CycleDirection | None = None
    video: VideoMode | None = None
    game: GameMode | None = None
    music: MusicMode | None = None
    hue_target: str | None = None


@dataclass
class ExecutionData(BaseModel):
    """State returned by the `/execution` endpoint."""

    sync_active: bool
    """False in powersave/passthrough; true while syncing in a sync mode."""
    mode: ExecutionMode
    last_sync_mode: SyncMode
    """Most recently used sync mode."""
    hue_target: str
    """Entertainment-area identifier, either `groups/<id>` or an entertainmentconfiguration UUID."""
    brightness: int
    """0 - 200 (100 = no brightness reduction/boost compared to input, 0 = max reduction, 200 = max boost)."""
    video: VideoMode
    game: GameMode
    music: MusicMode
    hdmi_active: bool | None = None
    """False in powersave; true while passing through or syncing HDMI content."""
    hdmi_source: HdmiSource | None = None
    """Currently selected HDMI input."""
    preset: str | None = None
    """Identifier of the preset currently being executed, when one is active."""
