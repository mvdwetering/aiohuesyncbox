from dataclasses import dataclass
from typing import Optional

from .base import BaseModel
from .enums import ExecutionMode, HdmiSource, Intensity, MusicPalette, SyncMode


@dataclass
class VideoMode(BaseModel):
    """Video (or game) mode execution state."""

    #: subtle, moderate, high, intense
    intensity: Intensity
    background_lighting: bool


@dataclass
class GameMode(VideoMode):
    pass


@dataclass
class MusicMode(BaseModel):
    """Music mode execution state."""

    #: subtle, moderate, high, intense
    intensity: Intensity
    #: happyEnergetic, happyCalm, melancholicCalm, melancholicEnergetic, neutral
    palette: MusicPalette


@dataclass
class ExecutionData(BaseModel):
    """Represent Execution config."""

    #: Reports false in case of powersave or passthrough mode,
    #: and true in case of video, game, or music mode.
    sync_active: bool
    #: Reports false in case of powersave mode,
    #: and true in case of passthrough, video, game or music mode.
    hdmi_active: bool
    #: powersave, passthrough, video, game, music, ambient
    #: (More modes can be added in the future, so clients must gracefully handle modes they don't recognize)
    mode: ExecutionMode
    #: Last sync mode used.
    last_sync_mode: SyncMode
    #: Current selected HDMI source input1, input2, input3, input4.
    hdmi_source: HdmiSource
    #: Currently selected entertainment area. Corresponds to a group under /hue. E.g. "groups/13"
    hue_target: str
    #: 0 - 200 (100 = no brightness reduction/boost compared to input, 0 = max reduction, 200 = max boost)
    brightness: int
    video: VideoMode
    game: GameMode
    music: MusicMode
    preset: Optional[str] = None
