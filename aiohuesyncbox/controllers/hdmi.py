from typing import TYPE_CHECKING

from ..models import HdmiData, Input, Output, RequestFunc
from .base import Resource


class Hdmi(Resource[HdmiData]):
    """Control the Hdmi resource of the huesyncbox."""

    if TYPE_CHECKING:
        # __getattr__ delegates these to self._data at runtime; declared here
        # only so type checkers see real types instead of Any.
        content_specs: str
        video_sync_supported: bool
        audio_sync_supported: bool
        output: Output
        input1: Input
        input2: Input
        input3: Input
        input4: Input

    def __init__(self, data: HdmiData, request: RequestFunc) -> None:
        super().__init__("/hdmi", data, request)
