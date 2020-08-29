from .helpers import generate_attribute_string

class Input():

    def __init__(self, id, raw):
        self.id = id
        self._raw = raw

    @property
    def name(self):
        """Friendly name of the input."""
        return self._raw['name']

    @property
    def type(self):
        """Type of the input."""
        return self._raw['type']

    @property
    def status(self):
        """Status of the input: unplugged, plugged, linked, unknown"""
        return self._raw['status']

    @property
    def last_sync_mode(self):
        """Last sync mode of the input."""
        return self._raw['lastSyncMode']


class Hdmi:
    """Represent Hdmi config of huesyncbox."""

    def __init__(self, raw, request):
        self._raw = raw
        self._request = request
        self._update_inputs_and_output()

    def __str__(self):
        attributes = ["content_specs", "video_sync_supported", "audio_sync_supported", "inputs", "output"]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        return self._raw == other._raw

    def _update_inputs_and_output(self):
        inputs = []
        for key, value in self._raw.items():
            if key.startswith('input'):
                inputs.append(Input(key, value))
        self._inputs = inputs
        self._output = Input('output', self._raw['output'])

    @property
    def content_specs(self):
        """Content specs of current input of huesyncbox."""
        return self._raw['contentSpecs']

    @property
    def video_sync_supported(self):
        """Indicates if syncing is supported on video content."""
        return self._raw['videoSyncSupported']

    @property
    def audio_sync_supported(self):
        """Indicates if syncing is supported on audio content."""
        return self._raw['audioSyncSupported']

    @property
    def inputs(self):
        """HDMI inputs of the huesyncbox."""
        return self._inputs

    @property
    def output(self):
        """HDMI output of the huesyncbox."""
        return self._output

    async def update(self):
        response = await self._request('get', '/hdmi')
        if response:
            self._raw = response
            self._update_inputs_and_output()