from dataclasses import dataclass

from .base import BaseModel, UpdateModel
from .enums import DeviceAction, LedMode, WifiState, WifiStrength


@dataclass
class Wifi(BaseModel):
    """Wi-Fi network state reported by the Sync Box."""

    ssid: str
    strength: WifiStrength


@dataclass
class DeviceAutoUpdate(BaseModel):
    """Automatic firmware update configuration."""

    auto_update_enabled: bool
    auto_update_time: int
    """UTC hour at which the Sync Box checks for and applies updates."""


@dataclass
class DeviceCapabilities(BaseModel):
    """Limits advertised by the Sync Box."""

    max_ir_codes: int
    max_presets: int


@dataclass
class DeviceUpdate(UpdateModel):
    """Mutable fields accepted by the `/device` endpoint."""

    name: str | None = None
    led_mode: LedMode | None = None
    action: DeviceAction | None = None
    update: DeviceAutoUpdate | None = None
    bluetooth: bool | None = None


@dataclass
class DeviceData(BaseModel):
    """State returned by the `/device` endpoint."""

    name: str
    """Friendly name of the device."""
    device_type: str
    """Device model identifier, e.g. HSB1."""
    unique_id: str
    """
    Capitalized hex string of the 6 byte/12 characters device id without delimiters. 
    Used as unique id on label, certificate common name, hostname etc.
    """
    ip_address: str
    """Local IP address of the device"""
    api_level: int
    """Increased between firmware versions when api changes."""
    firmware_version: str
    """User readable version of the device firmware, starting with decimal major .minor .maintenance format e.g. “1.12.3”"""
    build_number: int
    """Monotonically increasing firmware build number."""
    led_mode: LedMode
    wifi: Wifi | None = None
    """Connected Wi-Fi network information, when available."""
    wifi_state: WifiState | None = None
    updatable_firmware_version: str | None = None
    """Firmware version available to install, or `None` when current."""
    updatable_build_number: int | None = None
    """Build number available to install, or `None` when current."""
    last_checked_update: str | None = None
    """UTC ISO 8601 timestamp of the most recent update check."""
    update: DeviceAutoUpdate | None = None
    action: DeviceAction | None = None
    pushlink: str | None = None
    overheating: bool | None = None
    """Critical power-supply voltage warning reported by the Sync Box."""
    undervolt: bool | None = None
    """Critical power-supply voltage warning reported by the Sync Box."""
    bluetooth: bool | None = None
    capabilities: DeviceCapabilities | None = None
