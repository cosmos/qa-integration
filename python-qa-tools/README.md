This repo contains python scripts which can be used for quickly setting up a local test environment for any Cosmos based network with *n* number of nodes and *m* number of accounts. It installs **go** if it's not already installed on the system and also installs all the dependencies along with it.

## Install Python development environment on your system

```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-venv
```

## Create a virtual environment (recommended)

```bash
### Create a new virtual environment by choosing a Python interpreter and making a ./venv directory to hold it:
python3 -m venv --system-site-packages ./venv

### Activate the virtual environment using a shell-specific command:
source ./venv/bin/activate # When the virtual environment is active, your shell prompt is prefixed with (venv)
```

## Install packages and dependencies within a virtual environment without affecting the host system setup. Start by upgrading pip:

```bash
pip install --upgrade pip
git clone https://github.com/cosmos/qa-integration.git && cd qa-integration 
pip install -r requirements.txt
```

## To exit the virtual environment later:

```bash
deactivate  # don't exit until you're done using dependencies.
```

## Update env values in .env file

```bash
cp .env.example .env
```
> Note: A `.env.example` file is provided in the repo which contains default values of env variables. Edit the `.env` file with the values of your choice before executing any script.

```bash
DAEMON=simd
DENOM=uatom
CHAINID=test
DAEMON_HOME=${HOME}/.simd
GH_URL=https://github.com/cosmos/cosmos-sdk
CHAIN_VERSION='v0.45.1'
UPGRADE_NAME=test
UPGRADE_VERSION='v0.46.0-alpha4'
```

## Before running the scripts make sure to set the PYTHONPATH
> Note: $HOME/cosmos-qa-tools is customised.
```bash
echo 'export PYTHONPATH=$PYTHONPATH:$HOME/qa-integration/python-qa-tools' >> ~/.bashrc
source ~/.bashrc
```
## Scripts:-

1. `prereq.py` :- This script installs the basic apt packages and also checks if *go* is installed on the system or not. If *go* is not installed on the system then `go1.17.3` is installed by the script. Env variables related to *go* are also exported to bashrc.

Usage:- 
```bash
python3 deps/prereq.py
```

2. `cosmos_multinode.py` :- This script sets up the environment. It takes two arguments from the user. First argument is the number of nodes that need to be setup and the second argument is the number of additional accounts that need to be created.

Usage:-

```bash
python3 provision/cosmos_multinode.py --help
```
