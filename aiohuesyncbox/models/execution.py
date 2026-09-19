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
    """Reports false in case of powersave or passthrough mode, and true in case of video, game, or music mode."""
    toggle_sync_active: bool | None = None
    """true toggles boolean property value."""
    hdmi_active: bool | None = None
    """Reports false in case of powersave mode, and true in case of passthrough, video, game, or music mode."""
    toggle_hdmi_active: bool | None = None
    """true toggles boolean property value."""
    mode: ExecutionMode | None = None
    """powersave, passthrough, video, game, music."""
    cycle_sync_mode: CycleDirection | None = None
    """cycle enum property value forward or backward."""
    hdmi_source: HdmiSource | None = None
    """input1, input2, input3, input4 (currently selected hdmi input)."""
    cycle_hdmi_source: CycleDirection | None = None
    """cycle enum property value forward or backward."""
    brightness: int | None = None
    """0 - 200 (100 = no brightness reduction/boost compared to input, 0 = max reduction, 200 = max boost)."""
    increment_brightness: int | None = None
    """brightness delta."""
    intensity: Intensity | None = None
    """set intensity of current sync mode if syncing."""
    cycle_intensity: CycleDirection | None = None
    """cycle enum property value forward or backward."""
    toggle_sync_mode: SyncMode | None = None
    """Toggles into the given sync mode if not already active in that mode."""
    video: VideoMode | None = None
    game: GameMode | None = None
    music: MusicMode | None = None
    background_lighting: bool | None = None
    """Set background lighting of current sync mode if syncing."""
    toggle_background_lighting: bool | None = None
    """true toggles boolean property value."""
    hue_target: str | None = None
    """Currently selected entertainment area (entertainment configuration id for bridge api v2)."""
    preset: str | None = None
    """Preset identifier, that will be executed."""


@dataclass
class ExecutionData(BaseModel):
    """State returned by the `/execution` endpoint."""

    sync_active: bool
    """Reports false in case of powersave or passthrough mode, and true in case of video, game, or music mode."""
    mode: ExecutionMode
    """powersave, passthrough, video, game, music."""
    last_sync_mode: SyncMode
    """video, game, music."""
    hue_target: str
    """Currently selected entertainment area (entertainment configuration id for bridge api v2)."""
    brightness: int
    """0 - 200 (100 = no brightness reduction/boost compared to input, 0 = max reduction, 200 = max boost)."""
    video: VideoMode
    game: GameMode
    music: MusicMode
    hdmi_active: bool | None = None
    """Reports false in case of powersave mode, and true in case of passthrough, video, game, or music mode."""
    hdmi_source: HdmiSource | None = None
    """input1, input2, input3, input4 (currently selected hdmi input)."""
    preset: str | None = None
    """Preset identifier, that will be executed."""
