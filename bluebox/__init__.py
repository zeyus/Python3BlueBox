import typing as t
from .freqs import BaseMF, DTMF, MF

__version__ = '0.1.0'

_MF: t.Dict[str, t.Type[BaseMF]] = {}


def register_mf(name: str, backend: t.Type[BaseMF]) -> None:
    """Register a MF set."""
    _MF[name] = backend


def get_mf(name: str) -> t.Type[BaseMF]:
    """Get a MF set."""
    return _MF[name]


def list_mf() -> t.List[str]:
    """List the available MF sets."""
    return list(_MF.keys())


register_mf('dtmf', DTMF)
register_mf('mf', MF)
