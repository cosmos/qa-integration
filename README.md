## Cosmos QA tools

This repo contains scripts which can be used for quickly setting up a local test environment for any Cosmos based network with **n** number of nodes and **m** number of accounts.
It installs **go** if it's not already installed on the system and also installs all the dependencies along with it. 

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
UPGRADE_NAME=test
UPGRADE_VERSION='v0.46.0'
NUM_MSGS=30
RPC="http://localhost:16657"
```
>Note: Need not to export the env varibables using `export` command, These env values are fetched automatically by the scripts.

## Commands:

### Installation and Linting
```
make install-deps
make lint
```

### Chain setup
```
make setup-chain
make pause-chain
make resume-chain
make stop-chain
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

## More details about the scripts

### deps

`env-check.sh`:- This script is called before executing the other scripts ensuring that the env variables are properly imported.

    ```
    Usage:-

    chmod +x ./deps/env-check.sh
    ./deps/env-check.sh
    ```

`prereq.sh`:- This script is used to install all the dependencies and Go lang required to run the other scripts.

  ```
  Usage:-

  chmod +x ./deps/prereq.sh
  ./deps/prereq.sh
  ```

### Chain management

`start_chain.sh`:- This script sets up the environment. It takes two arguments from the user. First argument is the number of nodes that need to be setup and the second argument is the number of additional accounts that need to be created. 

  ```
  Usage:-

  git clone https://github.com/cosmos/qa-integration.git
  cd qa-integration
  chmod +x ./scripts/chain/start_chain.sh
  ./scripts/chain/start_chain.sh 2 2

  #This will create a network with 2 validators and 2 additional accounts. If the second argument is not passed, no new additional accounts are created. 
  #If no arguments are passed it creates a two node network by default.
  ```

`node_status.sh`:- This script displays the latest block height and sync status of the nodes.
 
 ```
 Usage:-

 chmod +x ./scripts/chain/node_status.sh
 ./scripts/chain/node_status.sh 5
 # This script takes one argument from user which specifies the number of validators for which the status will be displayed. If no argument is passed then it displays the status of the first node.
 ```

 `pause_nodes.sh`:- This script pauses the nodes.

 ```
 Usage:-

 chmod +x ./scripts/chain/pause_nodes.sh
 ./scripts/chain/pause_nodes.sh 5
 # This script takes one argument from the user which specifies the number of nodes to pause. If no argument is passed then just the first node will be paused.
 ```

 `resume_nodes.sh`:- This script starts the paused nodes.

 ```
 Usage:-

 chmod +x ./scripts/chain/resume_nodes.sh
 ./scripts/chain/resume_nodes.sh 5
  #This script takes one argument from the user which specifies the number of nodes to start back up. If no argument is passed then just the first node is started
  #back up.
 ```

 `shutdown_nodes.sh`:- This script shuts down the nodes and removes their respective home directories as well.

 ```
 Usage:-

 chmod +x ./scripts/chain/shutdown_nodes.sh
 ./scripts/chain/shutdown_nodes.sh 5
 #This script takes one argument from the user which specifies the number of nodes to shut down. If no argument is passed then just the first node is shut down.
 ```

`test_upgrade.sh`:- This script test the process of moving the upgraded version of binary from build folder to Cosmovisor's upgrades folder. This shell script takes one argument as NODE(Number of nodes to be upgraded).

```
  Usage:-

  chmod +x ./scripts/upgrade/test_upgrade.sh 2
  ./scripts/upgrade/test_upgrade.sh 2
```

### load-test

`multi_msg_load.sh`:- This script test a series of bank transfer transactions with multiple messages between two accounts. It takes two optional arguments namely -s(sender) and -r(receiver). 

  ```
  Usage:-

  chmod +x ./scripts/tests/multi_msg_load.sh
  ./scripts/tests/multi_msg_load.sh -h
  ./scripts/tests/multi_msg_load.sh -s <address> -r <address>
  ```

`query_load.sh`:- This script floods the network with balance queries, delegation queries and staking queries. It creates a load of 10,000 querires.

 ```
 Usage:-

 chmod +x query_load.sh
 ./query_load.sh
 ```

`send_load.sh`:- This script creates a load of 10,000 `send` transactions and floods the network.  

 ```
 Usage:-

 chmod +x send_load.sh
 ./send_load.sh 1 2
 #This script takes 2 arguments from the user which specifies the account number of `to` and `from` addresses. If no argument is passed then first and second address is taken by default.
 ```

`single_msg_load.sh`:- This script test a series of bank transfer transactions with single message between two accounts. It takes two optional arguments namely -s(sender) and -r(receiver). 

  ```
  Usage:-

  chmod +x ./scripts/tests/single_msg_load.sh
  ./scripts/tests/single_msg_load.sh -h
  ./scripts/tests/single_msg_load.sh -s <address> -r <address>
  ```
