"""Device Validation."""
# Standard Library Imports
from typing import Union

# Third Party Imports
from pydantic import AnyUrl
from pydantic import BaseModel
from pydantic import IPvAnyAddress
from pydantic import SecretStr
from pydantic import StrictBool
from pydantic import StrictInt
from pydantic import StrictStr


class Device(BaseModel):
    """Per-device validation model."""

    name: StrictStr
    host: Union[IPvAnyAddress, AnyUrl]
    port: StrictInt = 8080
    username: StrictStr
    password: SecretStr
    ssl: StrictBool = False

    def url(self):
        """Construct formatted http URL for interacting with device.

        Returns:
            {str} -- Formatted URL
        """
        if self.ssl:
            protocol = "https://"
        else:
            protocol = "http://"
        return f"{protocol}{self.host}:{self.port}"
