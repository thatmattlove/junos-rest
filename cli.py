#!/usr/bin/env python3

import asyncio

import click
import stackprinter
import ujson
import uvloop
from click import ClickException
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers.data import JsonLexer
from pygments.styles.monokai import MonokaiStyle

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
E = _Emoji()

# Click Style Helpers
SUCCESS = {"fg": "green", "bold": True}
ERROR = {"fg": "red", "bold": True}
LABEL = {"fg": "white"}
INFO = {"fg": "blue", "bold": True}
STATUS = {"fg": "black"}
VALUE = {"fg": "magenta", "bold": True}
CMD_HELP = {"fg": "white"}


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


if __name__ == "__main__":
    cli()
