from .helpers import generate_attribute_string

class SyncMode:
    """Sync mode. Only intensity for now so one class is enough"""
    def __init__(self, raw):
        self._raw = raw

    @property
    def intensity(self):
        """Intensity of the mode (subtle, moderate, high, intense)."""
        return self._raw['intensity']


class Execution:
    """Represent Execution config."""

    def __init__(self, raw, request):
        self._raw = raw
        self._request = request
        self._update_syncmodes()

    def __str__(self):
        attributes = ["sync_active", "hdmi_active", "mode", "last_sync_mode", "hdmi_source", "hue_target", "brightness", "video", "game", "music"]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        return self._raw == other._raw

    def _update_syncmodes(self):
        self._syncmode_video = SyncMode(self._raw['video'])
        self._syncmode_game = SyncMode(self._raw['game'])
        self._syncmode_music = SyncMode(self._raw['music'])

    async def _put(self, data):
        await self._request('put', '/execution', data=data)

    @property
    def sync_active(self):
        """
	    Reports false in case of powersave or passthrough mode,
        and true in case of video, game, or music mode.
        """
        return self._raw['syncActive']

    @property
    def hdmi_active(self):
        """Reports false in case of powersave mode,
        and true in case of passthrough, video, game or music mode.
        """
        return self._raw['hdmiActive']

    @property
    def mode(self):
        """
        powersave, passthrough, video, game, music, ambient (ambient is deprecated and will be removed in the future)
        (More modes can be added in the future, so clients must gracefully handle modes they don’t recognize)
        """
        return self._raw['mode']

    @property
    def last_sync_mode(self):
        """Last sync mode used."""
        return self._raw['lastSyncMode']

    @property
    def hdmi_source(self):
        """Current selected HDMI source input1, input2, input3, input4."""
        return self._raw['hdmiSource']

    @property
    def hue_target(self):
        """Currently selected entertainment area. Corresponds to a group under /hue. E.g. "groups/13" """
        return self._raw['hueTarget']

    @property
    def brightness(self):
        """
        Brightness of the huesyncbox.
        0 – 200 (100 = no brightness reduction/boost compared to input, 0 = max reduction, 200 = max boost)
        """
        return self._raw['brightness']

    @property
    def video(self):
        """Video mode execution state of the huesyncbox."""
        return self._syncmode_video

    @property
    def game(self):
        """Game mode execution state of the huesyncbox."""
        return self._syncmode_game

    @property
    def music(self):
        """Music mode execution state of the huesyncbox."""
        return self._syncmode_music

    async def toggle_sync_active(self):
        """Toggle sync_active."""
        data = {'toggleSyncActive': True}
        await self._put(data)

    async def toggle_hdmi_active(self):
        """Toggle hdmi_active."""
        data = {'toggleHdmiActive': True}
        await self._put(data)

    async def cycle_sync_mode(self, next=True):
        """Cycle through sync modes."""
        data = {'cycleSyncMode': 'next' if next else 'previous'}
        await self._put(data)

    async def cycle_hdmi_source(self, next=True):
        """Cycle through HDMI sources."""
        data = {'cycleHdmiSource': 'next' if next else 'previous'}
        await self._put(data)

    async def increment_brightness(self, step):
        """Increment brightness step should be within -200, 200."""
        data = {'incrementBrightness': step}
        await self._put(data)

    async def cycle_intensity(self, next=True):
        """Cycle through intensities of current mode if syncing."""
        data = {'cycleIntensity': 'next' if next else 'previous'}
        await self._put(data)

    async def set_intensity(self, intensity):
        """Set intensity (if syncing)."""
        data = {'intensity': intensity}
        await self._put(data)

    async def set_state(self, sync_active=None, sync_toggle=None, hdmi_active=None, hdmi_active_toggle=None, mode=None, mode_cycle=None, hdmi_source=None, hdmi_source_cycle=None, brightness=None, brightness_step=None, video=None, game=None, music=None, intensity=None, intensity_cycle=None, hue_target=None):
        """Change execution state of huesyncbox."""
        data = {
            key: value for key, value in {
                'syncActive': sync_active,
                'toggleSyncActive': True if sync_toggle is True else None,
                'hdmiActive': hdmi_active,
                'toggleHdmiActive': True if hdmi_active_toggle is True else None,
                'mode': mode,
                'cycleSyncMode': mode_cycle,
                'hdmiSource': hdmi_source,
                'cycleHdmiSource': hdmi_source_cycle,
                'brightness': brightness,
                'incrementBrightness': brightness_step,
                'intensity': intensity,
                'cycleIntensity': intensity_cycle,
                'video': video,
                'game': game,
                'music': music,
                'hueTarget': hue_target,
            }.items() if value is not None
        }
        await self._put(data)

    async def update(self):
        response = await self._request('get', '/execution')
        if response:
            self._raw = response
            self._update_syncmodes()

