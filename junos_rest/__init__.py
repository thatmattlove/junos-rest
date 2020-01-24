"""Get/Configure JunOS devices as if they had an actual REST API."""

# Standard Library Imports
import asyncio

# Third Party Imports
import stackprinter
import uvloop

__name__ = "junos_rest"

stackprinter.set_excepthook(style="darkbg2")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.get_event_loop()

print(f"\nStarting {__name__} with loop '{loop.__module__}'\n")
