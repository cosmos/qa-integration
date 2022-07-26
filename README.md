## Cosmos QA tools

This repo contains scripts which can be used for quickly setting up a local test environment for any Cosmos based network with **n** number of nodes and **m** number of accounts.

These scripts require a few env variables to be setup in ./env file:-

For eg:- 
```
goversion="1.18.1"
DAEMON=simd
DENOM=stake
CHAINID=test
DAEMON_HOME=${HOME}/.simd
GH_URL=https://github.com/cosmos/cosmos-sdk
CHAIN_VERSION='v0.45.4'
UPGRADE_NAME='v045-to-v046'
UPGRADE_VERSION='v0.46.0-rc2'
NUM_TXS=50
NUM_MSGS=30
RPC="http://localhost:16657"
MONGO_URL="mongodb://localhost:27017/"
DB_NAME=qa_test
NUM_VALS=3
UPGRADE_WAITING_TIME='10s'
IS_PUBLIC=false
```
>Note: Need not to export the env varibables using `export` command, These env values are fetched automatically by the scripts.

## Dependencies 
> Please install [docker](https://docs.docker.com/desktop/install/linux-install/) and [docker-compose](https://docs.docker.com/compose/install/)

## Commands:
### Installation and Linting
```bash
$ make install-deps
$ make lint
```

### Chain setup with docker 
```bash
$ make docker-build
$ make init-testnet
```

### Start the chain with docker-compose 
```bash
## Start the multinode chain 
$ make start-docker-chain

## Stop the multinode chain 
$ make stop-docker-chain

## ReStart the multinode chain 
$ make restart-docker-chain

```
### Tests

To execute all the tests
```
make test-all
```

To execute multi-msg load test
```
make test-multi-msg
```

To execute single-msg load test
```
make test-single-msg
```

To execute query load test
```
make test-query-load
```
