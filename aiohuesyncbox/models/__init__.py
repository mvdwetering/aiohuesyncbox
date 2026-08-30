"""Pure data models mirroring the Sync Box JSON API (mashumaro dataclasses, no I/O)."""

from .base import BaseModel as BaseModel
from .base import RequestFunc as RequestFunc
from .base import UpdateModel as UpdateModel

from .device import Wifi as Wifi
from .device import DeviceData as DeviceData
from .device import DeviceCapabilities as DeviceCapabilities
from .device import DeviceUpdate as DeviceUpdate
from .device import DeviceAutoUpdate as DeviceAutoUpdate

from .execution import VideoMode as VideoMode
from .execution import GameMode as GameMode
from .execution import MusicMode as MusicMode
from .execution import ExecutionData as ExecutionData
from .execution import ExecutionUpdate as ExecutionUpdate

from .hue import Group as Group
from .hue import HueData as HueData
from .hue import GroupUpdate as GroupUpdate
from .hue import HueUpdate as HueUpdate

from .hdmi import Port as Port
from .hdmi import Input as Input
from .hdmi import Output as Output
from .hdmi import HdmiData as HdmiData
from .hdmi import PortUpdate as PortUpdate

from .behavior import InputBehavior as InputBehavior
from .behavior import BehaviorData as BehaviorData
from .behavior import BehaviorUpdate as BehaviorUpdate

from .ir import ScanState as ScanState
from .ir import IrCode as IrCode
from .ir import IrData as IrData
from .ir import IrCodeUpdate as IrCodeUpdate
from .ir import ScanUpdate as ScanUpdate

from .registrations import Registration as Registration
from .registrations import RegistrationCreate as RegistrationCreate
from .registrations import RegistrationCredentials as RegistrationCredentials

from .presets import Preset as Preset
from .presets import PresetCreate as PresetCreate
from .presets import PresetUpdate as PresetUpdate

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
