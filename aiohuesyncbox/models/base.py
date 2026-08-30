"""Shared base for mashumaro dataclasses that mirror the Sync Box JSON API."""

import re
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from mashumaro.config import BaseConfig
from mashumaro.mixins.dict import DataClassDictMixin

_CAMEL_RE = re.compile(r"_([a-z0-9])")

RequestFunc = Callable[..., Awaitable[Any]]


def camel_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def snake_to_camel(name: str) -> str:
    return _CAMEL_RE.sub(lambda m: m.group(1).upper(), name)


@dataclass
class BaseModel(DataClassDictMixin):
    """Base for API models, translates camelCase JSON keys <-> snake_case fields."""

    class Config(BaseConfig):
        pass

    @classmethod
    def __pre_deserialize__(cls, d: dict[str, Any]) -> dict[str, Any]:
        return {camel_to_snake(key): value for key, value in d.items()}

    def __post_serialize__(self, d: dict[str, Any]) -> dict[str, Any]:
        return {snake_to_camel(key): value for key, value in d.items()}


@dataclass
class UpdateModel(BaseModel):
    """Base for partial API updates that omits unspecified fields."""

    class Config(BaseConfig):
        omit_none = True
