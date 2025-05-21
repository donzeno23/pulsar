# Pulsar

```text
custom toolkit for benchmarking
```

## install uv

```text
pulsar % curl -LsSf https://astral.sh/uv/install.sh | sh
downloading uv 0.6.17 aarch64-apple-darwin
no checksums to verify
installing to /Users/mdaloia/.local/bin
  uv
  uvx
everything's installed!

To add $HOME/.local/bin to your PATH, either restart your shell or run:

    source $HOME/.local/bin/env (sh, bash, zsh)
    source $HOME/.local/bin/env.fish (fish)
pulsar % source $HOME/.local/bin/env
```

## check uv installation

```text
(3.12.0) mdaloia@Michaels-Mac-mini pulsar % uv
An extremely fast Python package manager.

Usage: uv [OPTIONS] <COMMAND>

Commands:
  run      Run a command or script
  init     Create a new project
  add      Add dependencies to the project
  remove   Remove dependencies from the project
  sync     Update the project's environment
  lock     Update the project's lockfile
  export   Export the project's lockfile to an alternate format
  tree     Display the project's dependency tree
  tool     Run and install commands provided by Python packages
  python   Manage Python versions and installations
  pip      Manage Python packages with a pip-compatible interface
  venv     Create a virtual environment
  build    Build Python packages into source distributions and wheels
  publish  Upload distributions to an index
  cache    Manage uv's cache
  self     Manage the uv executable
  version  Display uv's version
  help     Display documentation for a command

Cache options:
  -n, --no-cache               Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation [env: UV_NO_CACHE=]
      --cache-dir <CACHE_DIR>  Path to the cache directory [env: UV_CACHE_DIR=]

Python options:
  --managed-python       Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
  --no-managed-python    Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
  --no-python-downloads  Disable automatic downloads of Python. [env: "UV_PYTHON_DOWNLOADS=never"]

Global options:
  -q, --quiet...                                   Use quiet output
  -v, --verbose...                                 Use verbose output
      --color <COLOR_CHOICE>                       Control the use of color in output [possible values: auto, always, never]
      --native-tls                                 Whether to load TLS certificates from the platform's native certificate store [env: UV_NATIVE_TLS=]
      --offline                                    Disable network access [env: UV_OFFLINE=]
      --allow-insecure-host <ALLOW_INSECURE_HOST>  Allow insecure connections to a host [env: UV_INSECURE_HOST=]
      --no-progress                                Hide all progress outputs [env: UV_NO_PROGRESS=]
      --directory <DIRECTORY>                      Change to the given directory prior to running the command
      --project <PROJECT>                          Run the command within the given project directory [env: UV_PROJECT=]
      --config-file <CONFIG_FILE>                  The path to a `uv.toml` file to use for configuration [env: UV_CONFIG_FILE=]
      --no-config                                  Avoid discovering configuration files (`pyproject.toml`, `uv.toml`) [env: UV_NO_CONFIG=]
  -h, --help                                       Display the concise help for this command
  -V, --version                                    Display the uv version

Use `uv help` for more details.
```

## Create virtual env and sync packages

```text
src $ uv sync
Using CPython 3.12.10
Creating virtual environment at: .venv
Resolved 89 packages in 3.03s
      Built pulsar @ file:///Users/<user>/sandbox/pulsar/src
      Built validators==0.20.0
      Built gherkin-official==4.1.3
Prepared 88 packages in 16.48s
Installed 88 packages in 2.17s
...
 + tzlocal==5.3.1
 + urllib3==2.4.0
 + validators==0.20.0
 + werkzeug==3.1.3
```

## Activate the virtual env

```text
src $ source .venv/bin/activate
(pulsar) $ 
```

## Install the pulsar package

```text
(3.12.0) src % uv run main.py 
Using CPython 3.12.0 interpreter at: /Users/mdaloia/.pyenv/versions/3.12.0/bin/python3.12
Creating virtual environment at: .venv
      Built pulsar @ file:///Users/mdaloia/Documents/GitHub/pulsar/src
Installed 88 packages in 775ms
Hello from src!
(3.12.0) mdaloia@Michaels-Mac-mini src % source .venv/bin/activate
(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % python
Python 3.12.0 (main, Nov 29 2023, 10:33:08) [Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pulsar
>>> from pulsar import get_logs
>>> from pulsar import stages
>>> from pulsar import loader
>>> 
```

## Alternative method: install the package in development mode

```text
(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % pwd
/Users/mdaloia/Documents/GitHub/pulsar/src

(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % uv pip install --editable .
Resolved 88 packages in 68ms
      Built pulsar @ file:///Users/mdaloia/Documents/GitHub/pulsar/src
Prepared 1 package in 205ms
Uninstalled 1 package in 0.67ms
Installed 1 package in 1ms
 ~ pulsar==0.1.0 (from file:///Users/mdaloia/Documents/GitHub/pulsar/src)
```

## Import the pulsar package

```text
(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % python
Python 3.12.0 (main, Nov 29 2023, 10:33:08) [Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pulsar
>>> from pulsar import get_logs
>>> from pulsar import send_messages
>>> from pulsar import loader
>>> from pulsar import stages
```

## Run test_plan

```text
(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini pulsar % cd src

(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % uv pip uninstall pulsar
Uninstalled 1 package in 9ms
 - pulsar==0.1.0 (from file:///Users/mdaloia/Documents/GitHub/pulsar/src)

(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % uv pip install -e .
Resolved 88 packages in 220ms
      Built pulsar @ file:///Users/mdaloia/Documents/GitHub/pulsar/src
Prepared 1 package in 263ms
Installed 1 package in 0.98ms
 + pulsar==0.1.0 (from file:///Users/mdaloia/Documents/GitHub/pulsar/src)

(pulsar) (3.12.0) mdaloia@Michaels-Mac-mini src % python -m pulsar.test_plan 
```

## Build package

```text
(pulsar) src $ uv sync
Resolved 89 packages in 30ms
      Built pulsar @ file:///Users/<user>/sandbox/pulsar/src
Prepared 1 package in 614ms
Uninstalled 1 package in 11ms
Installed 1 package in 4ms
 ~ pulsar==0.1.0 (from file:///Users/<user>/sandbox/pulsar/src)
```
