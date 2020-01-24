"""Application Configuration Validation."""
# Standard Library Imports
from typing import List

# Third Party Imports
from pydantic import BaseModel

# Project Imports
from junos_rest.models.device import Device


class Config(BaseModel):
    """Global app validatioin model."""

    devices: List[Device]
