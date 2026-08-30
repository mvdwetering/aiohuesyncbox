from typing import Optional

from ..models import ExecutionData, ExecutionUpdate, GameMode, MusicMode, RequestFunc, VideoMode
from ..models.enums import CycleDirection, ExecutionMode, HdmiSource, Intensity
from .base import Resource


class Execution(Resource[ExecutionData]):
    """Control the Execution resource of the huesyncbox."""

    def __init__(self, data: ExecutionData, request: RequestFunc) -> None:
        super().__init__("/execution", data, request)

    async def toggle_sync_active(self) -> None:
        """Toggle sync_active."""
        await self._put(ExecutionUpdate(toggle_sync_active=True).to_dict())

    async def toggle_hdmi_active(self) -> None:
        """Toggle hdmi_active."""
        await self._put(ExecutionUpdate(toggle_hdmi_active=True).to_dict())

    async def cycle_sync_mode(self, next: bool = True) -> None:
        """Cycle through sync modes."""
        direction = CycleDirection.NEXT if next else CycleDirection.PREVIOUS
        await self._put(ExecutionUpdate(cycle_sync_mode=direction).to_dict())

    async def cycle_hdmi_source(self, next: bool = True) -> None:
        """Cycle through HDMI sources."""
        direction = CycleDirection.NEXT if next else CycleDirection.PREVIOUS
        await self._put(ExecutionUpdate(cycle_hdmi_source=direction).to_dict())

    async def increment_brightness(self, step: int) -> None:
        """Increment brightness step should be within -200, 200."""
        await self._put(ExecutionUpdate(increment_brightness=step).to_dict())

    async def cycle_intensity(self, next: bool = True) -> None:
        """Cycle through intensities of current mode if syncing."""
        direction = CycleDirection.NEXT if next else CycleDirection.PREVIOUS
        await self._put(ExecutionUpdate(cycle_intensity=direction).to_dict())

    async def set_intensity(self, intensity: Intensity) -> None:
        """Set intensity (if syncing)."""
        await self._put(ExecutionUpdate(intensity=intensity).to_dict())

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
        update = ExecutionUpdate(
            sync_active=sync_active,
            toggle_sync_active=True if sync_toggle else None,
            hdmi_active=hdmi_active,
            toggle_hdmi_active=True if hdmi_active_toggle else None,
            mode=mode,
            cycle_sync_mode=mode_cycle,
            hdmi_source=hdmi_source,
            cycle_hdmi_source=hdmi_source_cycle,
            brightness=brightness,
            increment_brightness=brightness_step,
            intensity=intensity,
            cycle_intensity=intensity_cycle,
            video=video,
            game=game,
            music=music,
            hue_target=hue_target,
        )
        await self._put(update.to_dict())
