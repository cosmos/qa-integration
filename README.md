## Cosmos QA tools

This repo contains scripts which can be used for quickly setting up a local test environment for any Cosmos based network with **n** number of nodes and **m** number of accounts.
It installs **go** if it's not already installed on the system and also installs all the dependencies along with it. 

These scripts require a few env variables to be setup first such as:-

```
export DAEMON_HOME=<path to the home directory which will house the chain data>
export CHAINID=<chain-id of your test environment>
export DENOM=<denom of your token>
export GH_URL=<github url of the repository to clone>
export CHAIN_VERSION=<git tag to build>
export DAEMON=<binary name>
export UPGRADE_NAME=<upgrade name in handler>
export UPGRADE_VERSION=<git tag or branch name with upgrade handler>
```
For eg:- 
```
export DAEMON_HOME=~/.gaiad
export CHAINID=test
export DENOM=uatom
export GH_URL=https://github.com/cosmos/gaia
export CHAIN_VERSION=v6.0.0
export DAEMON=gaiad
export UPGRADE_NAME=v7.0-upgrade
export UPGRADE_VERSION=v7.0.0
```

### Scripts:-

1) `start_chain.sh`:- This script sets up the environment. It takes two arguments from the user.
First argument is the number of nodes that need to be setup and the second argument is the number of additional accounts that need to be created. 
Usage:-
 ```
 git clone https://github.com/cosmos/qa-integration.git
 cd qa-integration
 chmod +x provision/start_chain.sh
 ./provision/start_chain.sh 2 2
 ```
 This will create a network with 20 validators and 100 additional accounts. If the second argument is not passed, no new additional accounts are created. 
 If no arguments are passed it creates a two node network by default.

2) `multinode_distributions.sh`:- This script executes the distribuition mudule txs like `withdraw-rewards`,
 `withdraw-rewards --commission` and `withdraw-all-rewards`
 Usage:-
 ```
 chmod +x multinode_distributions.sh
 ./multinode_distributions.sh 5
 ```
 This script takes one argument from the user which specifies the number of validators on which the distribution txs are to be executed. If no argument is passed
 then it executes on the first two validators by default.
 
3) `multinode_staking.sh`:- This script executes the staking module txs like `delegate`, `redelegate` and `unbond`
 Usage:-
 ```
 chmod +x multinode_staking.sh
 ./multinode_staking.sh 5
 ```
 This script takes one argument from the user which specifies the number of validators on which the staking txs are to be executed. If no argument is passed
 then it executes on the first two validators by default.
 
4) `node_status.sh`:- This script displays the latest block height and sync status of the nodes.
 Usage:-
 ```
 chmod +x node_status.sh
 ./node_status.sh 5
 ```
 This script takes one argument from user which specifies the number of validators for which the status will be displayed. If no argument is passed then it displays 
 the status of the first node.
 
 5) `pause_nodes.sh`:- This script pauses the nodes.
  Usage:-
 ```
 chmod +x pause_nodes.sh
 ./pause_nodes.sh 5
 ```
 This script takes one argument from the user which specifies the number of nodes to pause. If no argument is passed then just the first node will be paused.
 
 6) `resume_nodes.sh`:- This script starts the paused nodes.
   Usage:-
 ```
 chmod +x resume_nodes.sh
 ./resume_nodes.sh 5
 ```
 This script takes one argument from the user which specifies the number of nodes to start back up. If no argument is passed then just the first node is started
 back up.
 
 7) `shutdown_nodes.sh`:- This script shuts down the nodes and removes their respective home directories as well.
   Usage:-
 ```
 chmod +x shutdown_nodes.sh
 ./shutdown_nodes.sh 5
 ``` 
 This script takes one argument from the user which specifies the number of nodes to shut down. If no argument is passed then just the first node is shut down.
 
 8) `send_load.sh`:- This script creates a load of 10,000 `send` transactions and floods the network.  
    Usage:-
 ```
 chmod +x send_load.sh
 ./send_load.sh 1 2
 ```
 This script takes 2 arguments from the user which specifies the account number of `to` and `from` addresses. If no argument is passed then first and second address is taken by default.
 
 9) `query_load.sh`:- This script floods the network with balance queries, delegation queries and staking queries. It creates a load of 10,000 querires.
     Usage:-
 ```
 chmod +x query_load.sh
 ./query_load.sh
 ```
 10) `setup_upgrade.sh`:- This script creates the necessary folders for cosmovisor. It also builds and places the binaries in the folders depending on the upgrade
name.
     Usage:-
 ```
 chmod +x setup_upgrade.sh
 ./setup_upgrade.sh 5

```
This script takes one argument from the user which specifies the number of nodes on which the setup needs to be completed.

