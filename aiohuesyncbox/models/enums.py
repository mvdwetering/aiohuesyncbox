"""Enumerated values defined by the Sync Box API."""

import logging
from enum import IntEnum, StrEnum

LOGGER = logging.getLogger(__name__)

UNKNOWN_STRING = "-- UNKNOWN API VALUE --"


class OpenStrEnum(StrEnum):
    """String enum that preserves unrecognized string values."""

    @classmethod
    def _missing_(cls, value: object) -> "OpenStrEnum | None":
        if not isinstance(value, str):
            return None
        LOGGER.warning("Unknown %s value received: %r", cls.__name__, value)
        return cls.__members__["UNKNOWN_API_VALUE"]


class WifiState(OpenStrEnum):
    UNINITIALIZED = "uninitialized"
    DISCONNECTED = "disconnected"
    LAN = "lan"
    WAN = "wan"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN"""


class WifiStrength(IntEnum):
    NOT_CONNECTED = 0
    WEAK = 1
    FAIR = 2
    GOOD = 3
    EXCELLENT = 4


class LedMode(IntEnum):
    OFF = 0
    REGULAR = 1
    DIMMED = 2


class DeviceAction(OpenStrEnum):
    NONE = "none"
    SOFTWARE_RESTART = "doSoftwareRestart"
    FIRMWARE_UPDATE = "doFirmwareUpdate"
    CHECK_FOR_FIRMWARE_UPDATES = "checkForFirmwareUpdates"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class ConnectionState(OpenStrEnum):
    UNINITIALIZED = "uninitialized"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    UNAUTHORIZED = "unauthorized"
    CONNECTED = "connected"
    INVALID_GROUP = "invalidgroup"
    STREAMING = "streaming"
    BUSY = "busy"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class OperatingMode(OpenStrEnum):
    UNINITIALIZED = "uninitialized"
    BRIDGE = "bridge"
    STANDALONE = "standalone"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class ExecutionMode(OpenStrEnum):
    POWERSAVE = "powersave"
    PASSTHROUGH = "passthrough"
    VIDEO = "video"
    GAME = "game"
    MUSIC = "music"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class SyncMode(OpenStrEnum):
    VIDEO = "video"
    GAME = "game"
    MUSIC = "music"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class HdmiSource(OpenStrEnum):
    INPUT1 = "input1"
    INPUT2 = "input2"
    INPUT3 = "input3"
    INPUT4 = "input4"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class Intensity(OpenStrEnum):
    SUBTLE = "subtle"
    MODERATE = "moderate"
    HIGH = "high"
    INTENSE = "intense"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class MusicPalette(OpenStrEnum):
    HAPPY_ENERGETIC = "happyEnergetic"
    HAPPY_CALM = "happyCalm"
    MELANCHOLIC_CALM = "melancholicCalm"
    MELANCHOLIC_ENERGETIC = "melancholicEnergetic"
    NEUTRAL = "neutral"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class CycleDirection(OpenStrEnum):
    NEXT = "next"
    PREVIOUS = "previous"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class PortType(OpenStrEnum):
    GENERIC = "generic"
    VIDEO = "video"
    GAME = "game"
    MUSIC = "music"
    XBOX = "xbox"
    PLAYSTATION = "playstation"
    NINTENDO_SWITCH = "nintendoswitch"
    PHONE = "phone"
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    APPLE_TV = "appletv"
    ROKU = "roku"
    SHIELD = "shield"
    CHROMECAST = "chromecast"
    FIRE_TV = "firetv"
    DISK_PLAYER = "diskplayer"
    SET_TOP_BOX = "settopbox"
    SATELLITE = "satellite"
    AV_RECEIVER = "avreceiver"
    SOUND_BAR = "soundbar"
    HDMI_SWITCH = "hdmiswitch"
    TV = "tv"
    MONITOR = "monitor"
    BEAMER = "beamer"
    SPEAKER = "speaker"
    HDMI_SPLITTER = "hdmisplitter"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class PortStatus(OpenStrEnum):
    UNPLUGGED = "unplugged"
    PLUGGED = "plugged"
    LINKED = "linked"
    UNKNOWN = "unknown"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""


class HdrMode(IntEnum):
    AUTO = 0
    FORCE_SDR = 1
    FORCE_HDR = 2


class RegistrationRole(OpenStrEnum):
    ADMIN = "admin"
    USER = "user"

    UNKNOWN_API_VALUE = UNKNOWN_STRING
    """Unknown string values in the enum are mapped to UNKNOWN_API_VALUE"""
