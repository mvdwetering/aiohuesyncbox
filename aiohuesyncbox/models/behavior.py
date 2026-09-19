from dataclasses import dataclass

from .base import BaseModel, UpdateModel
from .enums import HdrMode


@dataclass
class InputBehavior(BaseModel):
    """Root object for each of the 4 hdmi input subresources for HSB1 & HSB2 and for HSB3 only 1 hdmi input subresource."""

    cec_input_switch: bool
    """Automatically switch input when this source sends CEC active."""
    link_auto_sync: bool
    """Automatically set syncActive true when this source and output are linked."""
    hdr_mode: HdrMode | None = None
    """HSB1 - HDR PQ compensation during Light Sync. 0 = Auto; 1 = Force SDR; 2 = Force HDR; Default 0. Sync Box 4K only."""
    hpd_input_port_switch: bool | None = None
    """Automatically switch input when individual source is plugged in (or powered on). Added in API level 10."""


@dataclass
class BehaviorUpdate(UpdateModel):
    """Partial configuration change accepted by the `/behavior` endpoint."""

    inactive_powersave: int | None = None
    cec_powersave: bool | None = None
    usb_powersave: bool | None = None
    hpd_input_switch: bool | None = None
    arc_bypass_mode: bool | None = None
    solo_mode: bool | None = None
    """Added in API level 14."""
    force_dovi_native: bool | None = None
    input1: InputBehavior | None = None
    input2: InputBehavior | None = None
    input3: InputBehavior | None = None
    input4: InputBehavior | None = None


@dataclass
class BehaviorData(BaseModel):
    """Configuration returned by the `/behavior` endpoint."""

    inactive_powersave: int
    """Device automatically goes to powersave after this many minutes of being in passthrough mode with no link on any source or no link on output. 0 is disabled, max is 10000. Default 20."""
    cec_powersave: bool
    """Device goes to powersave when TV sends CEC OFF."""
    usb_powersave: bool | None = None
    """HSB1 & HSB2 - Device goes to powersave when USB power transitions from 5V to 0V."""
    hpd_input_switch: bool | None = None
    """HSB1 & HSB2 - Automatically switch input when any source is plugged in (or powered on)."""
    arc_bypass_mode: bool | None = None
    """Enable to make Sync Box's physical address transparent/invisible to source and TV. Must only be enabled when box is connected between an AVR and TV."""
    solo_mode: bool | None = None
    """Enable when Sync Box input is connected to the secondary output of an AV receiver (HDMI splitter) and the output is not connected. Added in API level 14."""
    force_dovi_native: bool | None = None
    """HSB1 - When the TV advertises Dolby Vision force to use native mode. Sync Box 4K only."""
    input1: InputBehavior | None = None
    input2: InputBehavior | None = None
    input3: InputBehavior | None = None
    input4: InputBehavior | None = None
