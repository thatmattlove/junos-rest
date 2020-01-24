"""HTTP Connection Handler."""
# Standard Library Imports
import asyncio

# Third Party Imports
import httpx

# Project Imports
from junos_rest.exceptions import JunosRestError
from junos_rest.log import log
from junos_rest.parser import parse_results


async def _test_reachability(host, port):
    """Verify the target host & port are actually reachable and open.

    Arguments:
        host {str} -- Device hostname or IP address
        port {int} -- Device listening TCP port

    Raises:
        JunosRestError: Raised if device is unreachable

    Returns:
        {bool} -- True if device is reachable
    """
    from socket import gaierror

    try:
        _reader, _writer = await asyncio.open_connection(str(host), int(port))
    except gaierror:
        raise JunosRestError(f"{host}:{port} is unreachable/unresolvable.", status=502)
    if _reader or _writer:
        return True
    else:
        return False


class Connection:
    """Create a reusable session to a JunOS device."""

    device = None
    session = None

    @classmethod
    async def new(cls, device):
        """Intantiate a connection to a JunOS device.

        Arguments:
            device {object} -- Device object

        Returns:
            {object} -- Initialized connection
        """
        instance = Connection()
        endpoint = device.url()

        reachable = await _test_reachability(device.host, device.port)

        if reachable:
            log.debug(f"'{device.name}' is reachable")

        common_http = {
            "base_url": endpoint,
            "verify": False,
            "auth": (device.username, device.password.get_secret_value()),
            "headers": {"Content-Type": "application/xml"},
        }

        instance.device = device
        instance.session = httpx.AsyncClient(**common_http)

        log.debug(f"Opened session with {device.host}")

        return instance

    async def close(self):
        """Close the session.

        Raises:
            JunosRestError: Raised if session is unable to be closed.
        """
        await self.session.aclose()

        if not self.session.dispatch.is_closed:
            raise JunosRestError(
                "Unable to close session with {device}", device=self.device
            )

        log.debug(f"Closed session with {self.device.host}")

    async def get(self, endpoint="/rpc", params=None):
        """Perform HTTP GET.

        Keyword Arguments:
            endpoint {str} -- HTTP URI (default: {"/rpc"})
            params {dict} -- URL Parameters (default: {None})

        Raises:
            JunosRestError: Raised if status code is not 200
            JunosRestError: Raised on other HTTP/library errors

        Returns:
            {dict} -- Dictionary of parsed XML response
        """
        request_config = {}

        if params is not None:
            request_config.update({"params": params})
        try:
            response = await self.session.get(endpoint, **request_config)

            if response.status_code != 200:
                status = httpx.status_codes.StatusCode(response.status_code)
                status_name = status.name.replace("_", " ")
                raise JunosRestError(
                    "{msg} - {url}",
                    status=status.value,
                    msg=status_name,
                    url=response.url,
                )
        except httpx.HTTPError as http_err:
            raise JunosRestError(str(http_err))

        parsed = await parse_results(response)
        return parsed

    async def post(self, endpoint="/rpc/", params=None, data=""):
        """Perform HTTP POST.

        Keyword Arguments:
            endpoint {str} -- HTTP URI (default: {"/rpc/"})
            params {dict} -- URL Parameters (default: {None})
            data {str} -- XML Content (default: {""})
        
        Raises:
            JunosRestError: Raised if status code is not 200
            JunosRestError: Raised on other HTTP/library errors

        Returns:
            {dict} -- Dictionary of parsed XML response
        """
        request_config = {"data": data}

        if params is not None:
            request_config.update({"params": params})
        try:
            response = await self.session.post(endpoint, **request_config)

            if response.status_code != 200:
                status = httpx.status_codes.StatusCode(response.status_code)
                raise JunosRestError(
                    "{msg} - {url}",
                    status=status.value,
                    msg=status.name.replace("_", " "),
                    url=response.url,
                )
        except httpx.HTTPError as http_err:
            raise JunosRestError(str(http_err))

        parsed = await parse_results(response)
        return parsed
