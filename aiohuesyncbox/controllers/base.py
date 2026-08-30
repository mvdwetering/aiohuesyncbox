"""Base 'controller' classes that bind pure data models to API paths + requests."""

from typing import Any, Dict, Generic, Iterator, Optional, Type, TypeVar

from ..models import BaseModel, RequestFunc

T = TypeVar("T", bound=BaseModel)
TItem = TypeVar("TItem", bound=BaseModel)


class Resource(Generic[T]):
    """Controller for a singleton API resource (e.g. /device, /execution).

    Binds a data model instance to its API path and the request function.
    Field access (e.g. `device.name`) is delegated to the wrapped data model,
    keeping serialization concerns (in the data model) separate from
    networking/mutation concerns (here).
    """

    def __init__(self, path: str, data: T, request: RequestFunc) -> None:
        self._path = path
        self._data = data
        self._request = request

    def __getattr__(self, name: str) -> Any:
        return getattr(self._data, name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Resource):
            return NotImplemented
        return self._data == other._data

    def __repr__(self) -> str:
        return repr(self._data)

    async def _put(self, data: Dict[str, Any]) -> None:
        await self._request("put", self._path, data=data)

    async def update(self) -> None:
        """Refresh from the device."""
        response = await self._request("get", self._path)
        if response:
            self._data = type(self._data).from_dict(response)


class CollectionResource(Generic[TItem]):
    """Controller for map-style API resources where the GET response root
    itself is a `{id: item}` map (e.g. /registrations, /presets).
    """

    def __init__(self, path: str, item_cls: Type[TItem], request: RequestFunc) -> None:
        self._path = path
        self._item_cls = item_cls
        self._request = request
        self._items: Dict[str, TItem] = {}

    def __iter__(self) -> Iterator[TItem]:
        return iter(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, id: str) -> TItem:
        return self._items[id]

    def __contains__(self, id: str) -> bool:
        return id in self._items

    def get(self, id: str) -> Optional[TItem]:
        return self._items.get(id)

    async def update(self) -> None:
        """Refresh from the device."""
        response = await self._request("get", self._path)
        if response:
            self.load(response)

    def load(self, response: Dict[str, Any]) -> None:
        """Populate items from an already-fetched `{id: item}` response."""
        items = {}
        for id, raw in response.items():
            item = self._item_cls.from_dict(raw)
            item.id = id  # type: ignore[attr-defined]
            items[id] = item
        self._items = items

    async def delete(self, id: str) -> None:
        await self._request("delete", f"{self._path}/{id}")
