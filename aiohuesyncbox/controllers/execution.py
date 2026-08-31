from typing import TYPE_CHECKING

from ..models import ExecutionData, ExecutionUpdate, GameMode, MusicMode, RequestFunc, VideoMode
from ..models.enums import CycleDirection, ExecutionMode, HdmiSource, Intensity, SyncMode
from .base import Resource


class Execution(Resource[ExecutionData]):
    """Control the Execution resource of the huesyncbox."""

    if TYPE_CHECKING:
        # __getattr__ delegates these to self._data at runtime; declared here
        # so type checkers see real types instead of Any.
        sync_active: bool
        hdmi_active: bool
        mode: ExecutionMode
        last_sync_mode: SyncMode
        hdmi_source: HdmiSource
        hue_target: str
        brightness: int
        video: VideoMode
        game: GameMode
        music: MusicMode
        preset: str | None

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
        sync_active: bool | None = None,
        sync_toggle: bool | None = None,
        hdmi_active: bool | None = None,
        hdmi_active_toggle: bool | None = None,
        mode: ExecutionMode | None = None,
        mode_cycle: CycleDirection | None = None,
        hdmi_source: HdmiSource | None = None,
        hdmi_source_cycle: CycleDirection | None = None,
        brightness: int | None = None,
        brightness_step: int | None = None,
        video: VideoMode | None = None,
        game: GameMode | None = None,
        music: MusicMode | None = None,
        intensity: Intensity | None = None,
        intensity_cycle: CycleDirection | None = None,
        hue_target: str | None = None,
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
