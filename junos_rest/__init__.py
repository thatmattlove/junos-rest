"""Get/Configure JunOS devices as if they had an actual REST API."""

# Third Party Imports
import stackprinter
import uvloop

__name__ = "junos_rest"

stackprinter.set_excepthook(style="darkbg2")

uvloop.install()
