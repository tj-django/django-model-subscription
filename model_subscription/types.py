from typing import TypeVar, Callable, Any

T = TypeVar("T", bound=Callable[..., Any])
