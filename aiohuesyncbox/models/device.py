from dataclasses import dataclass
from typing import Optional

from .base import BaseModel
from .enums import DeviceAction, LedMode, WifiState, WifiStrength


@dataclass
class Wifi(BaseModel):
    """Represent wifi status"""

    ssid: str
    #: 0 = not connected; 1 = weak; 2 = fair; 3 = good; 4 = excellent
    strength: WifiStrength


@dataclass
class DeviceUpdate(BaseModel):
    auto_update_enabled: bool
    auto_update_time: int


@dataclass
class DeviceCapabilities(BaseModel):
    max_ir_codes: int
    max_presets: int


@dataclass
class DeviceData(BaseModel):
    """Represent Device config."""

    name: str
    device_type: str
    #: Capitalized hex string of the 6 byte / 12 characters device id without
    #: delimiters. Used as unique id on label, certificate common name, hostname etc.
    unique_id: str
    ip_address: str
    api_level: int
    firmware_version: str
    build_number: int
    #: 0 = off in powersave, passthrough or sync mode; 1 = regular;
    #: 2 = dimmed in powersave or passthrough mode and off in sync mode
    led_mode: LedMode
    wifi: Optional[Wifi] = None
    wifi_state: Optional[WifiState] = None
    updatable_firmware_version: Optional[str] = None
    updatable_build_number: Optional[int] = None
    last_checked_update: Optional[str] = None
    update: Optional[DeviceUpdate] = None
    action: Optional[DeviceAction] = None
    pushlink: Optional[str] = None
    overheating: Optional[bool] = None
    undervolt: Optional[bool] = None
    bluetooth: Optional[bool] = None
    capabilities: Optional[DeviceCapabilities] = None
