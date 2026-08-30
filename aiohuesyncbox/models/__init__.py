"""Pure data models mirroring the Sync Box JSON API (mashumaro dataclasses, no I/O)."""

from .base import BaseModel as BaseModel
from .base import RequestFunc as RequestFunc

from .device import Wifi as Wifi
from .device import DeviceData as DeviceData
from .device import DeviceCapabilities as DeviceCapabilities
from .device import DeviceUpdate as DeviceUpdate

from .execution import VideoMode as VideoMode
from .execution import GameMode as GameMode
from .execution import MusicMode as MusicMode
from .execution import ExecutionData as ExecutionData

from .hue import Group as Group
from .hue import HueData as HueData

from .hdmi import Port as Port
from .hdmi import Input as Input
from .hdmi import Output as Output
from .hdmi import HdmiData as HdmiData

from .behavior import InputBehavior as InputBehavior
from .behavior import BehaviorData as BehaviorData

from .ir import ScanState as ScanState
from .ir import IrCode as IrCode
from .ir import IrData as IrData

from .registrations import Registration as Registration

from .presets import Preset as Preset

from .enums import ConnectionState as ConnectionState
from .enums import CycleDirection as CycleDirection
from .enums import DeviceAction as DeviceAction
from .enums import Enabled as Enabled
from .enums import ExecutionMode as ExecutionMode
from .enums import HdmiSource as HdmiSource
from .enums import HdrMode as HdrMode
from .enums import Intensity as Intensity
from .enums import LedMode as LedMode
from .enums import MusicPalette as MusicPalette
from .enums import PortStatus as PortStatus
from .enums import PortType as PortType
from .enums import RegistrationRole as RegistrationRole
from .enums import SyncMode as SyncMode
from .enums import WifiState as WifiState
from .enums import WifiStrength as WifiStrength
