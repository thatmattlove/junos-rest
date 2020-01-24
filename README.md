# JunOS REST

**WORK IN PROGRESS**

JunOS REST is a library/CLI/API for interacting with Juniper JunOS devices without having to deal with the headache of XML.

The ultimate goal is to be able to take CLI output from `show configuration | display json`, load it into this library, and have that configuration magically appear on your Juniper device.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![SCC Line Count](https://sloc.xyz/github/checktheroads/junos-rest/?category=code)](https://github.com/boyter/scc/)

## Installation

**Requires Python 3.6+**

### [Install poetry](https://python-poetry.org/docs/):

```bash
curl https://pyenv.run | bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
```

### Clone Repository & Install dependencies

```bash
git clone https://github.com/checktheroads/junos-rest.git
cd junos-rest
poetry install --no-dev
```

## Configuration

The configuration is held in a YAML file located at `junos-rest/junos_rest/config.yaml`. Its model is strictly validated as:

```yaml
devices:
  - name: <device name> # String
    host: <device hostname or address> # String
    port: <device port> # Integer
    username: <device username> # String
    password: <device password> # String
```

For each additional device, another stanza can be added under the `devices:` key.

## Usage

Currently, as this is a work in progress, there are two ways to use this:

### CLI

*From* `junos-rest`
```bash
$ ./cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  configure  Send a new config

$ ./cli.py configure --help
Usage: cli.py configure [OPTIONS]

  Send a new config

Options:
  -d, --device TEXT  Device Name
  -c, --config TEXT  Configuration in JSON
  --help             Show this message and exit.

# Example: to set the device's timezone, run:
$ ./cli.py configure -d <device name> -c '{"system": {"time-zone": "Etc/UTC"}}'
```

And you'll get something like this:

```js
{
  "status":"success",
  "data":null
}
```

### Python API

Or, you can integrate with an existing application:

```python
import json
from junos_rest.actions import set_config

results = await set_config(
    device="<device name>",
    config={
        "system": {
            "time-zone": "Etc/UTC"
        }
    }
)
print(results)
# {"status": "success", "data": None}
```

#### asyncio

You might notice the `await` syntax above. If you're not familiar, [have a read](https://docs.python.org/3/library/asyncio.html). I do not intend to make a synchronous API available for this library. If you need to run junos-rest synchronously, try this:

```python
import asyncio

results = asyncio.run(set_config(...))
```

# License

<a href="http://www.wtfpl.net/"><img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" alt="WTFPL" /></a>