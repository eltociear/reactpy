from __future__ import annotations

import os
from typing import Any, Callable, Generic, TypeVar

_O = TypeVar("_O")


class Option(Generic[_O]):
    """An option that can be set using an environment variable of the same name"""

    def __init__(
        self,
        name: str,
        default: _O,
        allow_changes: bool = True,
        validator: Callable[[Any], _O] = lambda x: x,
    ) -> None:
        self.name = name
        self._default = default
        self._allow_changes = allow_changes
        self._validator = validator
        self._value = validator(os.environ.get(name, default))

    def get(self) -> _O:
        return self._value

    def set(self, new: _O) -> _O:
        if not self._allow_changes:
            raise ValueError(f"{self.name} cannot be modified.")
        old = self._value
        self._value = self._validator(new)
        return old

    def reset(self) -> _O:
        return self.set(self._default)
