"""Load YAML Config & Validate."""

# Standard Library Imports
from pathlib import Path

# Third Party Imports
import yaml

# Project Imports
from junos_rest.models.config import Config

WORKING_DIR = Path(__file__).parent
CONFIG_FILE = WORKING_DIR / "config.yaml"

if not CONFIG_FILE.exists():
    CONFIG_FILE = WORKING_DIR / "config.yml"

if CONFIG_FILE.exists():
    with CONFIG_FILE.open("r") as raw:
        unvalidated_config = yaml.safe_load(raw.read())
else:
    raise Exception("No config file found.")

params = Config(**unvalidated_config)
