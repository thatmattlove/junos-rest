"""Supported Interactions with JunOS Devices."""

# Standard Library Imports
import ujson

# Project Imports
from junos_rest.connection import Connection
from junos_rest.constants import CONFIG_JSON
from junos_rest.util import build_config
from junos_rest.util import find_device
from junos_rest.exceptions import JunosRestError


async def set_config(device, config=None, json_config=None):
    """Send a new configuration to a device.

    Arguments:
        device {str} -- Device Name
        config {dict} -- Configuration

    Returns:
        {dict} -- Response Details
    """
    if config is None and json_config is not None:
        config_data = await build_config(config=ujson.loads(json_config))
    elif config is not None and json_config is None:
        config_data = await build_config(config=config)
    elif config is not None and json_config is not None:
        config_data = await build_config(config=config)
    else:
        raise JunosRestError("A configuration must be specified.")

    device = await find_device(device_name=device)
    session = await Connection.new(device=device)

    current_config = await session.get(item="get-configuration")
    if "@" in current_config["configuration"]:
        current_config["configuration"].pop("@")

    json_config = ujson.dumps(config_data, escape_forward_slashes=False)

    result = await session.post(data=CONFIG_JSON.format(config=json_config).strip())
    return result
