"""Load YAML Config & Validate."""

# Standard Library Imports
from pathlib import Path

# Third Party Imports
import yaml

# Project Imports
from junos_rest.models.config import Config

WORKING_DIR = Path(__file__).parent
POTENTIAL_CONFIG_LOCATIONS = [
    Path.home(),
    Path("/etc/junos-rest/"),
    Path(__file__).parent.parent,
    Path(__file__).parent,
]

_matched_config_file = None
for path in POTENTIAL_CONFIG_LOCATIONS:
    file_path = path / "junos_rest.yaml"
    if file_path.exists():
        _matched_config_file = file_path
        break

if _matched_config_file is None:
    raise Exception(
        "No config file found. A file named 'junos_rest.yaml' must exist in one of the following paths: {p}".format(
            p=", ".join([str(p) for p in POTENTIAL_CONFIG_LOCATIONS])
        )
    )
with _matched_config_file.open("r") as raw:
    unvalidated_config = yaml.safe_load(raw.read())

params = Config(**unvalidated_config)
