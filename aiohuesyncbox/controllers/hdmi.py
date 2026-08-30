from ..models import HdmiData, RequestFunc
from .base import Resource


class Hdmi(Resource[HdmiData]):
    """Control the Hdmi resource of the huesyncbox."""

    def __init__(self, data: HdmiData, request: RequestFunc) -> None:
        super().__init__("/hdmi", data, request)
