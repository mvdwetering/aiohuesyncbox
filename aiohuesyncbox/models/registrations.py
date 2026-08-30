from dataclasses import dataclass, field

from .base import BaseModel
from .enums import RegistrationRole


@dataclass
class Registration(BaseModel):
    """Represent a single registered application/instance."""

    app_name: str
    instance_name: str
    #: UTC time when this registration was created.
    created: str
    #: UTC time when this registration was last used.
    last_used: str
    #: admin or user
    role: RegistrationRole

    #: Not part of the JSON body, it is the dict key under the registrations map.
    id: str = field(default="", compare=False, metadata={"serialize": "omit"})
