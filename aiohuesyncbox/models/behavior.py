from dataclasses import dataclass
from typing import Optional

from .base import BaseModel
from .enums import Enabled, HdrMode


@dataclass
class InputBehavior(BaseModel):
    """Per-HDMI-input behavior settings."""

    #: Automatically switch input when this source sends CEC active. Disabled 0, Enabled 1.
    cec_input_switch: Enabled
    #: Automatically set syncActive true when this source and output are linked. Disabled 0, Enabled 1.
    link_auto_sync: Enabled
    #: HDR PQ compensation during Light Sync. 0 = Auto; 1 = Force SDR; 2 = Force HDR. Sync Box 4K only.
    hdr_mode: Optional[HdrMode] = None
    #: Automatically switch input when individual source is plugged in (or powered on). Disabled 0, Enabled 1.
    hpd_input_port_switch: Optional[Enabled] = None


@dataclass
class BehaviorData(BaseModel):
    """Represent Behavior config of huesyncbox."""

    #: Minutes of no link before automatically going to powersave. 0 is disabled.
    inactive_powersave: int
    #: Go to powersave when TV sends CEC OFF. Disabled 0, Enabled 1.
    cec_powersave: Enabled
    #: Go to powersave when USB power transitions from 5V to 0V. Disabled 0, Enabled 1.
    usb_powersave: Enabled
    #: Automatically switch input when any source is plugged in (or powered on). Disabled 0, Enabled 1.
    hpd_input_switch: Enabled
    #: Force native mode when the TV advertises Dolby Vision. Sync Box 4K only.
    force_dovi_native: Optional[Enabled] = None
    input1: Optional[InputBehavior] = None
    input2: Optional[InputBehavior] = None
    input3: Optional[InputBehavior] = None
    input4: Optional[InputBehavior] = None
