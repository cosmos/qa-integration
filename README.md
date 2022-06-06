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

### Commands:
```
make install-deps
make lint
```

## Scripts:-

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

### provison

`start_chain.sh`:- This script sets up the environment. It takes two arguments from the user. First argument is the number of nodes that need to be setup and the second argument is the number of additional accounts that need to be created. 

  ```
  Usage:-

  git clone https://github.com/cosmos/qa-integration.git
  cd qa-integration
  chmod +x provision/start_chain.sh
  ./provision/start_chain.sh 2 2

  #This will create a network with 2 validators and 2 additional accounts. If the second argument is not passed, no new additional accounts are created. 
  #If no arguments are passed it creates a two node network by default.
  ```

`test_upgrade.sh`:- This script test the process of moving the upgraded version of binary from build folder to Cosmovisor's upgrades folder. This shell script    takes one argument as NODE(Number of nodes to be upgraded).

```
  Usage:-

  chmod +x ./provision/test_upgrade.sh 2
  ./provision/test_upgrade.sh 2

```

### load-test

`multi_msg_load.sh`:- This script test a series of bank transfer transactions with multiple messages between two accounts. It takes two optional arguments namely -s(sender) and -r(receiver). 

  ```
  Usage:-

  chmod +x ./load-test/multi_msg_load.sh
  ./load-test/multi_msg_load.sh -h
  ./load-test/multi_msg_load.sh -s <address> -r <address>
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

  chmod +x ./load-test/single_msg_load.sh
  ./load-test/single_msg_load.sh -h
  ./load-test/single_msg_load.sh -s <address> -r <address>
  ```

### misc-scripts

`distribution.sh`:- This script executes the distribuition mudule txs like `withdraw-rewards`, `withdraw-rewards --commission` and `withdraw-all-rewards`

  ```
  Usage:-

  chmod +x ./misc-scripts/distribution.sh
  ./misc-scripts/distribution.sh 5
  # This script takes one argument from the user which specifies the number of validators on which the distribution txs are to be executed. If no argument is passed then it executes on the first two #validators by default.
  ```

`proposal_vote.sh`:- This script test the gov module commands and sub commands.

  ```
  Usage:-

  chmod +x ./misc-scripts/proposal_vote.sh
  ./misc-scripts/proposal_vote.sh
  ```
 
`staking.sh`:- This script executes the staking module txs like `delegate`, `redelegate` and `unbond`.

 ```
 Usage:-

 chmod +x ./misc-scripts/staking.sh
 ./misc-scripts/staking.sh 5
 # This script takes one argument from the user which specifies the number of validators on which the staking txs are to be executed. If no argument is passed
 #then it executes on the first two validators by default.
 ```

 ### node-management
 
`node_status.sh`:- This script displays the latest block height and sync status of the nodes.
 
 ```
 Usage:-

 chmod +x node_status.sh
 ./node_status.sh 5
 # This script takes one argument from user which specifies the number of validators for which the status will be displayed. If no argument is passed then it displays the status of the first node.
 ```
 `pause_nodes.sh`:- This script pauses the nodes.

 ```
 Usage:-

 chmod +x pause_nodes.sh
 ./pause_nodes.sh 5
 # This script takes one argument from the user which specifies the number of nodes to pause. If no argument is passed then just the first node will be paused.
 ```

 `resume_nodes.sh`:- This script starts the paused nodes.

 ```
 Usage:-

 chmod +x resume_nodes.sh
 ./resume_nodes.sh 5
  #This script takes one argument from the user which specifies the number of nodes to start back up. If no argument is passed then just the first node is started
  #back up.
 ```

 
 
 `shutdown_nodes.sh`:- This script shuts down the nodes and removes their respective home directories as well.

 ```
 Usage:-

 chmod +x shutdown_nodes.sh
 ./shutdown_nodes.sh 5
 #This script takes one argument from the user which specifies the number of nodes to shut down. If no argument is passed then just the first node is shut down.
 ```

 `setup_upgrade.sh`:- This script creates the necessary folders for cosmovisor. It also builds and places the binaries in the folders depending on the upgrade name.
 ```
 Usage:-

 chmod +x setup_upgrade.sh
 ./setup_upgrade.sh 5

```
