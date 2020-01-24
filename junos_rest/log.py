"""Log handling."""

# Standard Library Imports
import sys

# Third Party Imports
from loguru import logger as _loguru_logger

_LOG_FMT = (
    "<lvl><b>[{level}]</b> {time:YYYYMMDD} {time:HH:mm:ss} <lw>|</lw> {name}<lw>:</lw>"
    "<b>{line}</b> <lw>|</lw> {function}</lvl> <lvl><b>→</b></lvl> {message}"
)
_LOG_LEVELS = [
    {"name": "DEBUG", "no": 10, "color": "<c>"},
    {"name": "INFO", "no": 20, "color": "<le>"},
    {"name": "SUCCESS", "no": 25, "color": "<g>"},
    {"name": "WARNING", "no": 30, "color": "<y>"},
    {"name": "ERROR", "no": 40, "color": "<y>"},
    {"name": "CRITICAL", "no": 50, "color": "<r>"},
]

_LOG_HANDLER = {"sink": sys.stdout, "format": _LOG_FMT, "level": "DEBUG"}


def _logger():
    _loguru_logger.remove()
    _loguru_logger.configure(handlers=[_LOG_HANDLER], levels=_LOG_LEVELS)
    return _loguru_logger


log = _logger()
