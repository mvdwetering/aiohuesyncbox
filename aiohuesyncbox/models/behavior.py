from dataclasses import dataclass

from .base import BaseModel, UpdateModel
from .enums import Enabled, HdrMode


@dataclass
class InputBehavior(BaseModel):
    """Per-HDMI-input behavior settings."""

    cec_input_switch: Enabled
    """Switch input when this source sends a CEC active signal."""
    link_auto_sync: Enabled
    """Start syncing when this input and the output are linked."""
    hdr_mode: HdrMode | None = None
    """HDR PQ compensation mode; supported by 4K Sync Boxes only."""
    hpd_input_port_switch: Enabled | None = None
    """Switch input when this source is connected or powered on."""


@dataclass
class BehaviorUpdate(UpdateModel):
    """Partial configuration change accepted by the `/behavior` endpoint."""

    inactive_powersave: int | None = None
    cec_powersave: Enabled | None = None
    usb_powersave: Enabled | None = None
    hpd_input_switch: Enabled | None = None
    force_dovi_native: Enabled | None = None
    input1: InputBehavior | None = None
    input2: InputBehavior | None = None
    input3: InputBehavior | None = None
    input4: InputBehavior | None = None


@dataclass
class BehaviorData(BaseModel):
    """Configuration returned by the `/behavior` endpoint."""

    inactive_powersave: int
    """Passthrough idle minutes before powersave; 0 disables the timeout."""
    cec_powersave: Enabled
    """Enter powersave when the TV sends a CEC off signal."""
    usb_powersave: Enabled | None = None
    """Enter powersave when USB power transitions from 5 V to 0 V."""
    hpd_input_switch: Enabled | None = None
    """Switch to an input when any source is connected or powered on."""
    force_dovi_native: Enabled | None = None
    """Force native Dolby Vision mode when advertised by the TV; 4K only."""
    input1: InputBehavior | None = None
    input2: InputBehavior | None = None
    input3: InputBehavior | None = None
    input4: InputBehavior | None = None
