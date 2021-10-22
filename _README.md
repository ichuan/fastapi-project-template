# {TITLE}
Python 3.9+


## Developing

### Install

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Running

```sh
# Choose a clean dir for data (db, logs, etc)
cd /path/to/a/clean/dir
# Create and init data dir (data)
python -m {PACKAGE}.bin.init data
# Create tables first
# DATA_DIR is the previously created dir. Use absolute path if running from elsewhere
DATA_DIR=data python -m {PACKAGE}.bin.cmd create tables
# Run the dev web server
DATA_DIR=`pwd`/data python -m {PACKAGE}.web
# Others commands is in
DATA_DIR=`pwd`/data python -m {PACKAGE}.bin.cmd
```

## Build

Optional: modify `VERSION` in `setup.py`

```sh
pip install setuptools wheel
python setup.py bdist_wheel
```

`dist/*.whl` will be the compiled package


## Deploy and Running

First, copy the `.whl` package to a remote server (with python 3.9+ installed).

### Install

```sh
# Choose a clean dir for env and data (db, logs, etc)
cd /path/to/a/clean/dir
# Create python env
python3 -m venv env
source env/bin/activate
# Install {PACKAGE}
pip install /path/to/{PACKAGE}-0.1.0-py3-none-any.whl
# Install supervisor
pip install supervisor
# Create data dir
python -m {PACKAGE}.bin.init data
# Create tables first
DATA_DIR=data python -m {PACKAGE}.bin.cmd create tables
```

### Running

Optional: modify `config/supervisord.ini` in `DATA_DIR`

```sh
# Run with supervisor
supervisord -c `pwd`/data/config/supervisord.ini
# Managing
supervisorctl -c `pwd`/data/config/supervisord.ini
# Others commands is in
DATA_DIR=`pwd`/data python -m {PACKAGE}.bin.cmd
```

When running from scripts or crontab, `supervisord` can be written as `env/bin/supervisord` (under the clean project dir)


## FAQ
- `PermissionError: [Errno 13] error while attempting to bind on address ('0.0.0.0', 443): permission denied`
  - ```sudo setcap 'cap_net_bind_service=+ep' `readlink -f $(which python)` ```
