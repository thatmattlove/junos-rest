"""Utility functions."""

# Third Party Imports
import ujson

# Project Imports
from junos_rest.config import params
from junos_rest.constants import CONFIG_JSON
from junos_rest.exceptions import JunosRestError
from junos_rest.log import log


def highlight(data, format="json"):
    """Format & syntax-highlight input data.

    Arguments:
        data {any} -- Data to Format
        format {str} -- Data syntax

    Returns:
        {str} -- Formatted ouput
    """
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter
    from pygments.lexers import get_lexer_by_name
    from pygments.styles.monokai import MonokaiStyle

    lexer = get_lexer_by_name(format)
    raw = format
    if format == "json":
        raw = ujson.dumps(data, indent=2, escape_forward_slashes=False)

    return highlight(raw, lexer, Terminal256Formatter(style=MonokaiStyle))


async def find_device(device_name):
    """Match an input device name with a configured device.

    Arguments:
        device_name {str} -- Device name

    Raises:
        JunosRestError: Raised if there is no matching device.

    Returns:
        {object} -- Matched device objcet
    """
    matched = None
    for device in params.devices:
        if device.name == device_name:
            matched = device
            break
    if matched is None:
        raise JunosRestError("No configured device matches {d}", d=device_name)
    return matched


async def build_config(config):
    """Wrap input config dict in proper JunOS XML tags, format as JSON.

    Arguments:
        config {dict} -- Configuration to push

    Returns:
        {str} -- Formatted XML data
    """

    parsed = {}

    if "configuration" not in config:
        parsed.update({"configuration": config})
    else:
        parsed.update(config)

    json_config = ujson.dumps(parsed, escape_forward_slashes=False)

    log.debug("Pending Config:\n{c}", c=highlight(data=parsed))
    return CONFIG_JSON.format(config=json_config).strip()
