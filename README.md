# JunOS REST

**Note: This is very much a work in progress.**

I'm deploying a bunch of Juniper routers and refuse to artisanally hand-craft either the initial configs or the operational changes of my big ass routing policy.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![SCC Line Count](https://sloc.xyz/github/checktheroads/hyperglass/?category=code)](https://github.com/boyter/scc/)

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

# License

<a href="http://www.wtfpl.net/"><img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" alt="WTFPL" /></a>