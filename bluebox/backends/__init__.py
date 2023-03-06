import typing as t
from .base import BlueboxBackend as BlueboxBackend  # noqa: F401
from .backend_pyaudio import PyAudioBackend as PyAudioBackend  # noqa: F401

_BACKENDS: t.Dict[str, t.Type[BlueboxBackend]] = {}


def register_backend(name: str, backend: t.Type[BlueboxBackend]) -> None:
    """Register a backend."""
    _BACKENDS[name] = backend


def get_backend(name: str) -> t.Type[BlueboxBackend]:
    """Get a backend."""
    return _BACKENDS[name]


def list_backends() -> t.List[str]:
    """List the available backends."""
    return list(_BACKENDS.keys())


register_backend('pyaudio', PyAudioBackend)
