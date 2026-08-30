from dataclasses import dataclass, field

from .base import BaseModel
from .enums import RegistrationRole


@dataclass
class Registration(BaseModel):
    """Registered application instance."""

    app_name: str
    """User-recognizable application name."""
    instance_name: str
    """
    User recognizable name of application instance. 
    Either a user name if single registration for user is shared over devices, 
    or device name if each device uses a separate registration.
    """
    created: str
    """UTC ISO 8601 timestamp at which the registration was created."""
    last_used: str
    """UTC ISO 8601 timestamp at which the registration was last used."""
    role: RegistrationRole
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})
    """Registration id derived from the containing registrations map key."""


@dataclass
class RegistrationCreate(BaseModel):
    """Payload accepted by `POST /registrations`, which requires pushlink."""

    app_name: str
    """User-recognizable application name."""
    instance_name: str
    """User name or device name associated with the registration."""
