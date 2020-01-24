"""Supported Interactions with JunOS Devices."""

# Project Imports
from junos_rest.connection import Connection
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
    result = await session.post(data=config_data)

    return result
