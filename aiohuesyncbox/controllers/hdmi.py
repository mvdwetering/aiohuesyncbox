from ..models import HdmiData, Input, Output, RequestFunc
from .base import Resource


class Hdmi(Resource[HdmiData]):
    """Control the Hdmi resource of the huesyncbox."""

    def __init__(self, data: HdmiData, request: RequestFunc) -> None:
        super().__init__("/hdmi", data, request)

    @property
    def content_specs(self) -> str:
        return self._data.content_specs

    @property
    def video_sync_supported(self) -> bool:
        return self._data.video_sync_supported

    @property
    def audio_sync_supported(self) -> bool:
        return self._data.audio_sync_supported

    @property
    def output(self) -> Output:
        return self._data.output

    @property
    def input1(self) -> Input:
        return self._data.input1

    @property
    def input2(self) -> Input | None:
        return self._data.input2

    @property
    def input3(self) -> Input | None:
        return self._data.input3

    @property
    def input4(self) -> Input | None:
        return self._data.input4
