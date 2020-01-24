"""Custom Application Exception(s)."""

# Third Party Imports
import ujson

# Project Imports
from junos_rest.log import log


class JunosRestError(Exception):
    """junos_rest base exception."""

    def __init__(self, message="", status=500, **kwargs):
        """Initialize the junos_rest base exception class.

        Keyword Arguments:
            message {str} -- Error message (default: {""})
            status {int} -- HTTP Status Code (default: {500})
        """
        self._message = message.format(**kwargs)
        self._status = status

        if self._status in range(400, 500):
            log.error(repr(self))

        elif self._status in range(500, 600):
            log.critical(repr(self))

        else:
            log.info(repr(self))

    def __str__(self):
        """Return the instance's error message.

        Returns:
            {str} -- Error Message
        """
        return self._message

    def __repr__(self):
        """Return the instance's severity & error message in a string.

        Returns:
            {str} -- Error message with code
        """
        return f"[{self._status}] {self._message}"

    def dict(self):
        """Return the instance's attributes as a dictionary.

        Returns:
            {dict} -- Exception attributes in dict
        """
        return {"message": self._message, "status": self._status}

    def json(self):
        """Return the instance's attributes as a JSON object.

        Returns:
            {str} -- Exception attributes as JSON
        """
        return ujson.dumps(self.dict())

    @property
    def message(self):
        """Return the instance's `message` attribute.

        Returns:
            {str} -- Error Message
        """
        return self._message

    @property
    def status(self):
        """Return the instance's `status` attribute.

        Returns:
            {int} -- HTTP Status Code
        """
        return self._status
