from typing import Dict, List
from .helpers import generate_attribute_string

INPUTS = ["input1", "input2", "input3", "input4"]


class Input:
    def __init__(self, raw: Dict) -> None:
        self._raw = raw

    @property
    def name(self) -> str:
        """Friendly name of the input."""
        return self._raw["name"]

    @property
    def type(self) -> str:
        """Type of the input."""
        return self._raw["type"]

    @property
    def status(self) -> str:
        """Status of the input: unplugged, plugged, linked, unknown"""
        return self._raw["status"]

    @property
    def last_sync_mode(self) -> str:
        """Last sync mode of the input."""
        return self._raw["lastSyncMode"]


class Output(Input):
    pass


class Hdmi:
    """Represent Hdmi config of huesyncbox."""

    def __init__(self, raw, request) -> None:
        self._raw = raw
        self._request = request
        self._update_inputs_and_output()

    def __str__(self):
        attributes = [
            "content_specs",
            "video_sync_supported",
            "audio_sync_supported",
            "inputs",
            "output",
        ]
        return generate_attribute_string(self, attributes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hdmi):
            return NotImplemented
        return self._raw == other._raw

    def _update_inputs_and_output(self) -> None:
        for input_id in INPUTS:
            if input_id in self._raw:
                input = Input(self._raw[input_id])
                setattr(self, f"_{input_id}", input)
        self._output = Output(self._raw["output"])

    @property
    def content_specs(self) -> str:
        """Content specs of current input of huesyncbox."""
        return self._raw["contentSpecs"]

    @property
    def video_sync_supported(self) -> bool:
        """Indicates if syncing is supported on video content."""
        return self._raw["videoSyncSupported"]

    @property
    def audio_sync_supported(self) -> bool:
        """Indicates if syncing is supported on audio content."""
        return self._raw["audioSyncSupported"]

    @property
    def input1(self) -> Input:
        """HDMI input 1 of the huesyncbox."""
        return getattr(self, "_input1")

    @property
    def input2(self) -> Input:
        """HDMI input 2 of the huesyncbox."""
        return getattr(self, "_input2")

    @property
    def input3(self) -> Input:
        """HDMI input 3 of the huesyncbox."""
        return getattr(self, "_input3")

    @property
    def input4(self) -> Input:
        """HDMI input 4 of the huesyncbox."""
        return getattr(self, "_input4")

    @property
    def output(self) -> Output:
        """HDMI output of the huesyncbox."""
        return self._output

    async def update(self) -> None:
        response = await self._request("get", "/hdmi")
        if response:
            self._raw = response
            self._update_inputs_and_output()
