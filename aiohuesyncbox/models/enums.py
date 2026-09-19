"""Enumerated values defined by the Sync Box API."""

from enum import IntEnum, StrEnum


class OpenStrEnum(StrEnum):
    """String enum that preserves unrecognized string values."""

    @classmethod
    def _missing_(cls, value: object) -> "OpenStrEnum | None":
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value.upper()
        member._value_ = value
        cls._value2member_map_[value] = member
        return member


class WifiState(StrEnum):
    UNINITIALIZED = "uninitialized"
    DISCONNECTED = "disconnected"
    LAN = "lan"
    WAN = "wan"


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


class ConnectionState(StrEnum):
    UNINITIALIZED = "uninitialized"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    UNAUTHORIZED = "unauthorized"
    CONNECTED = "connected"
    INVALID_GROUP = "invalidgroup"
    STREAMING = "streaming"
    BUSY = "busy"


class OperatingMode(OpenStrEnum):
    UNINITIALIZED = "uninitialized"
    BRIDGE = "bridge"
    STANDALONE = "standalone"


class ExecutionMode(OpenStrEnum):
    POWERSAVE = "powersave"
    PASSTHROUGH = "passthrough"
    VIDEO = "video"
    GAME = "game"
    MUSIC = "music"


class SyncMode(StrEnum):
    VIDEO = "video"
    GAME = "game"
    MUSIC = "music"


class HdmiSource(StrEnum):
    INPUT1 = "input1"
    INPUT2 = "input2"
    INPUT3 = "input3"
    INPUT4 = "input4"


class Intensity(StrEnum):
    SUBTLE = "subtle"
    MODERATE = "moderate"
    HIGH = "high"
    INTENSE = "intense"


class MusicPalette(StrEnum):
    HAPPY_ENERGETIC = "happyEnergetic"
    HAPPY_CALM = "happyCalm"
    MELANCHOLIC_CALM = "melancholicCalm"
    MELANCHOLIC_ENERGETIC = "melancholicEnergetic"
    NEUTRAL = "neutral"


class CycleDirection(StrEnum):
    NEXT = "next"
    PREVIOUS = "previous"


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


class PortStatus(OpenStrEnum):
    UNPLUGGED = "unplugged"
    PLUGGED = "plugged"
    LINKED = "linked"
    UNKNOWN = "unknown"


class HdrMode(IntEnum):
    AUTO = 0
    FORCE_SDR = 1
    FORCE_HDR = 2


class RegistrationRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
