from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=Callable[..., Any])
