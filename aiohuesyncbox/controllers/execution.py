from typing import Optional

from ..models import ExecutionData, GameMode, MusicMode, RequestFunc, VideoMode
from ..models.enums import CycleDirection, ExecutionMode, HdmiSource, Intensity
from .base import Resource


class Execution(Resource[ExecutionData]):
    """Control the Execution resource of the huesyncbox."""

    def __init__(self, data: ExecutionData, request: RequestFunc) -> None:
        super().__init__("/execution", data, request)

    async def toggle_sync_active(self) -> None:
        """Toggle sync_active."""
        await self._put({"toggleSyncActive": True})

    async def toggle_hdmi_active(self) -> None:
        """Toggle hdmi_active."""
        await self._put({"toggleHdmiActive": True})

    async def cycle_sync_mode(self, next: bool = True) -> None:
        """Cycle through sync modes."""
        await self._put({"cycleSyncMode": "next" if next else "previous"})

    async def cycle_hdmi_source(self, next: bool = True) -> None:
        """Cycle through HDMI sources."""
        await self._put({"cycleHdmiSource": "next" if next else "previous"})

    async def increment_brightness(self, step: int) -> None:
        """Increment brightness step should be within -200, 200."""
        await self._put({"incrementBrightness": step})

    async def cycle_intensity(self, next: bool = True) -> None:
        """Cycle through intensities of current mode if syncing."""
        await self._put({"cycleIntensity": "next" if next else "previous"})

    async def set_intensity(self, intensity: Intensity) -> None:
        """Set intensity (if syncing)."""
        await self._put({"intensity": intensity})

    async def set_state(
        self,
        sync_active: Optional[bool] = None,
        sync_toggle: Optional[bool] = None,
        hdmi_active: Optional[bool] = None,
        hdmi_active_toggle: Optional[bool] = None,
        mode: Optional[ExecutionMode] = None,
        mode_cycle: Optional[CycleDirection] = None,
        hdmi_source: Optional[HdmiSource] = None,
        hdmi_source_cycle: Optional[CycleDirection] = None,
        brightness: Optional[int] = None,
        brightness_step: Optional[int] = None,
        video: Optional[VideoMode] = None,
        game: Optional[GameMode] = None,
        music: Optional[MusicMode] = None,
        intensity: Optional[Intensity] = None,
        intensity_cycle: Optional[CycleDirection] = None,
        hue_target: Optional[str] = None,
    ) -> None:
        """Change execution state of huesyncbox."""
        data = {
            key: value
            for key, value in {
                "syncActive": sync_active,
                "toggleSyncActive": True if sync_toggle is True else None,
                "hdmiActive": hdmi_active,
                "toggleHdmiActive": True if hdmi_active_toggle is True else None,
                "mode": mode,
                "cycleSyncMode": mode_cycle,
                "hdmiSource": hdmi_source,
                "cycleHdmiSource": hdmi_source_cycle,
                "brightness": brightness,
                "incrementBrightness": brightness_step,
                "intensity": intensity,
                "cycleIntensity": intensity_cycle,
                "video": video.to_dict() if video else None,
                "game": game.to_dict() if game else None,
                "music": music.to_dict() if music else None,
                "hueTarget": hue_target,
            }.items()
            if value is not None
        }
        await self._put(data)
