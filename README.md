# Cosmos QA tools

This repo contains scripts which can be used for quickly setting up a local test environment for any Cosmos based network with **n** number of nodes and **m** number of accounts.
It installs **go** if it's not already installed on the system and also installs all the dependencies along with it.

These scripts require a few env variables to be setup in ./env file:-

For eg:-

```shell
goversion="1.18.1"
DAEMON=simd
DENOM=stake
CHAINID=test
DAEMON_HOME=${HOME}/.simd
GH_URL=https://github.com/cosmos/cosmos-sdk
CHAIN_VERSION='v0.45.4'
UPGRADE_NAME=test
UPGRADE_VERSION='v0.46.0'
NUM_TXS=50
NUM_MSGS=30
RPC="http://localhost:16657"
```

>Note: Need not to export the env varibables using `export` command, These env values are fetched automatically by the scripts.

## Commands

### Installation and Linting

```shell
make install-deps
make lint
```

### Chain setup

```shell
make setup-chain
make pause-chain
make resume-chain
make stop-chain
```

### Tests

To execute all the tests

```shell
make test-all
```

To execute multi-msg load test

```shell
make test-multi-msg
```

To execute single-msg load test

```shell
make test-single-msg
```

To execute query load test

```shell
make test-query-load
```
