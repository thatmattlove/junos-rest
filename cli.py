#!/usr/bin/env python3

import asyncio
import random

import click
import stackprinter
import ujson
import uvloop
from click import ClickException
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.data import JsonLexer
from pygments.styles.monokai import MonokaiStyle
from rapidtables import FORMAT_GENERATOR
from rapidtables import format_table

stackprinter.set_excepthook(style="darkbg2")
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class _Char:
    """Helper class for single-character strings."""

    def __init__(self, char):
        """Set instance character."""
        self.char = char

    def __getitem__(self, i):
        """Subscription returns the instance's character * n."""
        return self.char * i

    def __str__(self):
        """Stringify the instance character."""
        return str(self.char)

    def __repr__(self):
        """Stringify the instance character for representation."""
        return str(self.char)

    def __add__(self, other):
        """Addition method for string concatenation."""
        return str(self.char) + str(other)


class _Emoji:
    """Helper class for unicode emoji."""

    CHECK = "\U00002705 "
    INFO = "\U00002755 "
    ERROR = "\U0000274C "


WS = _Char(" ")
NL = _Char("\n")
CL = _Char(":")
DASH = _Char("-")
E = _Emoji()

# Click Style Helpers
SUCCESS = {"fg": "green", "bold": True}
ERROR = {"fg": "red", "bold": True}
LABEL = {"fg": "white", "bold": True}
INFO = {"fg": "blue", "bold": True}
STATUS = {"fg": "black"}
VALUE = {"fg": "magenta", "bold": True}
CMD_HELP = {"fg": "white"}
TITLE = {"fg": "white", "bold": True, "underline": True}


def async_command(func):
    """Decororator for to make async functions runable from syncronous code."""
    import asyncio
    from functools import update_wrapper

    func = asyncio.coroutine(func)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return update_wrapper(wrapper, func)


def highlighted_json(raw):
    """Format & Syntax-Highlight Dict as JSON.

    Arguments:
        raw {dict} -- Dictionary to Format

    Returns:
        {str} -- Formatted JSON
    """
    raw_json = ujson.dumps(raw, indent=2)
    return highlight(raw_json, JsonLexer(), Terminal256Formatter(style=MonokaiStyle))


def random_colors(rows):
    """From tuple of commands, generate random but unique colors."""
    colors = ["blue", "green", "red", "yellow", "magenta", "cyan", "white"]
    rows_list = list(rows)

    num_colors = len(colors)
    num_rows = len(rows_list)

    if num_rows >= num_colors:
        colors += colors

    unique_colors = random.sample(colors, num_rows)
    colored_rows = []

    for i, row in enumerate(rows_list):
        colored_rows.append(click.style(row, fg=unique_colors[i]))

    return colored_rows


@click.group()
def cli():
    pass


@cli.command("configure", help="Send a new config")
@click.option("-d", "--device", type=str, help="Device Name")
@click.option("-c", "--config", type=str, help="Configuration in JSON")
@async_command
async def send_config(device, config):
    from junos_rest.actions import set_config

    try:
        loaded_config = ujson.loads(config)
    except ValueError:
        raise ClickException(E.ERROR + click.style(f"'{config}' is not valid JSON"))

    results = await set_config(device=device, config=loaded_config)

    click.echo(NL[1] + E.CHECK + NL[2] + highlighted_json(results))


@cli.command("list", help="List configured devices")
def list_devices():
    from junos_rest.config import params

    devices = [d.dict(exclude={"password"}) for d in params.devices]
    try:
        header, rows = format_table(devices, fmt=FORMAT_GENERATOR, separator=WS[4])

        click.echo(
            click.style("Configured Devices", **TITLE)
            + NL[2]
            + click.style(header, **LABEL)
            + NL[1]
            + click.style(DASH[len(header)], **CMD_HELP)
        )
        for row in random_colors(rows):
            click.echo(row)
        click.echo(NL[0])

    except Exception as e:
        raise ClickException(str(e))


if __name__ == "__main__":
    cli()
