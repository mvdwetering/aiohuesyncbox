from dataclasses import dataclass
from typing import Optional

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

    name: Optional[str] = None
    led_mode: Optional[LedMode] = None
    action: Optional[DeviceAction] = None
    update: Optional[DeviceAutoUpdate] = None
    bluetooth: Optional[bool] = None


@dataclass
class DeviceData(BaseModel):
    """State returned by the `/device` endpoint."""

    name: str
    device_type: str
    """Device model identifier; new Sync Box models may introduce new values."""
    unique_id: str
    """
    Uppercase 12-character device identifier used on the label,
    certificate common name, and hostname.
    """
    ip_address: str
    api_level: int
    """API compatibility level reported by the installed firmware."""
    firmware_version: str
    """User-readable firmware version."""
    build_number: int
    """Monotonically increasing firmware build number."""
    led_mode: LedMode
    wifi: Optional[Wifi] = None
    """Connected Wi-Fi network information, when available."""
    wifi_state: Optional[WifiState] = None
    updatable_firmware_version: Optional[str] = None
    """Firmware version available to install, or `None` when current."""
    updatable_build_number: Optional[int] = None
    """Build number available to install, or `None` when current."""
    last_checked_update: Optional[str] = None
    """UTC ISO 8601 timestamp of the most recent update check."""
    update: Optional[DeviceAutoUpdate] = None
    action: Optional[DeviceAction] = None
    pushlink: Optional[str] = None
    overheating: Optional[bool] = None
    """Critical power-supply voltage warning reported by the Sync Box."""
    undervolt: Optional[bool] = None
    """Critical power-supply voltage warning reported by the Sync Box."""
    bluetooth: Optional[bool] = None
    capabilities: Optional[DeviceCapabilities] = None
