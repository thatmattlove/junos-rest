"""Supported Interactions with JunOS Devices."""

# Standard Library Imports
import json

# Project Imports
from junos_rest.connection import Connection
from junos_rest.constants import CONFIG_JSON
from junos_rest.util import build_config
from junos_rest.util import find_device


async def set_config(device, config):
    """Send a new configuration to a device.

    Arguments:
        device {str} -- Device Name
        config {dict} -- Configuration

    Returns:
        {dict} -- Response Details
    """
    device = await find_device(device_name=device)
    session = await Connection.new(device=device)
    config_data = await build_config(config=config)
    current_config = await session.get(item="get-configuration")
    if "@" in current_config["configuration"]:
        current_config["configuration"].pop("@")

    json_config = json.dumps(config_data, escape_forward_slashes=False)

    result = await session.post(data=CONFIG_JSON.format(config=json_config).strip())
    return result
