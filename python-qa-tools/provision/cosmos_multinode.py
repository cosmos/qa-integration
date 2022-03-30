import argparse, os, subprocess, sys, shutil, requests

from dotenv import dotenv_values
from subprocess import check_output
from utils.commands import is_tool

from utils.types import node_type

#Fetch env values
config = dotenv_values(".env")
DAEMON = config['DAEMON']
DENOM = config['DENOM']
CHAINID = config['CHAINID']
DAEMON_HOME = config['DAEMON_HOME']
GH_URL = config['GH_URL']
CHAIN_VERSION = config['CHAIN_VERSION']
HOME = os.getenv('HOME')
USER = os.getenv('USER')

### Fetch NODES and ACCOUNTS values
parser = argparse.ArgumentParser(description='This program takes inputs for setting up the required number of nodes.')
parser.add_argument('nodes', type= node_type, help= 'Number of nodes to be set up. Min. 2 should be given')
parser.add_argument('accounts', type= int, help= 'Number of Accounts to be set up. If not please enter 0')
args = parser.parse_args()
print(f" ** Number of nodes : {args.nodes} and accounts : {args.accounts} to be setup **") 
NODES, ACCOUNTS = str(args.nodes), str(args.accounts)
os.chdir(os.path.expanduser(HOME))

### Cosmosvisor installation
print("--------- Install cosmovisor-------")
if is_tool('cosmovisor'):
    print("Found cosmovisor already installed.\n")
    print("Skipping the cosmosvisor installation.\n")
else:
    subprocess.run(['go', 'install', 'github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0'])

subprocess.run(['which', 'cosmovisor']) # Print the cosmovisor location
if not GH_URL:
    sys.exit('The environment varible \'GH_URL\' is not set. make sure to update the env values in .env file')

REPO = GH_URL.split('/')[-1]

### DENOM Installation
print(f"--------- Install {DAEMON} ---------")
if is_tool(DAEMON):
    print(f"Found {DAEMON} already installed.\n")
    print(f"Skipping the {DAEMON} installation.\n")
else:
    git = {
        'clone' : f"git clone {GH_URL}",
        'fetch' : 'git fetch',
        'checkout' : f"git checkout {CHAIN_VERSION}",
        'install' : 'make install'
    }
    subprocess.run(git['clone'].split())
    os.chdir(REPO)
    subprocess.run(git['fetch'].split())
    subprocess.run(git['checkout'].split())
    subprocess.run(git['install'].split())
    
os.chdir(os.path.expanduser(HOME))
subprocess.run([f"{DAEMON}", 'version', '--long']) # check DAEMON version

### export daemon home paths
for i in range(1, int(NODES) + 1):
    os.environ[f'{DAEMON_HOME}_{i}'] = f"{DAEMON_HOME}-{i}"
    print(f"Deamon path :: {DAEMON_HOME}-{i}\n")
    print(f"****** here command {DAEMON} unsafe-reset-all  --home {DAEMON_HOME}-{i} ******")

### Remove the systemd services if they are already running ###
print(f"--------- Checking the existing system services running on {DAEMON}. -------------")
service_files = [f"{DAEMON}-{i}.service" for i in range(1, int(NODES) + 1)]
directory_path = "/lib/systemd/system"
for file in os.listdir(directory_path):
    if file in service_files:
        os.system(f"systemctl stop {file}")
        os.system(f"systemctl disable {file}")
        os.remove(os.path.join(directory_path, file))
        print(f"Removed {file} ")

### remove daemon home directories if it already exists ###
for i in range(1, int(NODES) + 1):
    try:
        shutil.rmtree(f"{DAEMON_HOME}-{i}")
        print(f"Deleting existing daemon directory {DAEMON_HOME}-{i}")
    except FileNotFoundError:
        print(f"The directory {DAEMON_HOME}-{i} does not exists")

### Creating daemon home directories
print("-----Creating daemon home directories------")
for i in range(1, int(NODES)+1):
    print(f"****** create dir :: {DAEMON_HOME}-{i} ********\n")
    try:
        os.mkdir(f"{DAEMON_HOME}-{i}")
        os.makedirs(f"{DAEMON_HOME}-{i}/cosmovisor/genesis/bin")
    except FileExistsError as e:
        print(e)
    except FileNotFoundError as e:
        sys.exit(e) 
    shutil.copy(src=f"{shutil.which(DAEMON)}", dst=f"{DAEMON_HOME}-{i}/cosmovisor/genesis/bin/")

### --------Start initializing the chain CHAINID ---------
print(f"--------Start initializing the chain {CHAINID}---------")
for i in range(1, int(NODES)+1):
    print(f"-------Init chain {i}--------")
    print(f"Deamon home :: {DAEMON_HOME}-{i}")
    subprocess.run([f"{DAEMON}", 'init', '--chain-id', f"{CHAINID}", f"{DAEMON_HOME}-{i}", '--home', f"{DAEMON_HOME}-{i}"])

### ------------Creating $NODES keys---------------
print(f"---------Creating {NODES} keys-------------")
for i in range(1, int(NODES) + 1):
    subprocess.run([f"{DAEMON}", 'keys', 'add', f"validator{i}", '--keyring-backend', 'test', '--home', f"{DAEMON_HOME}-{i}"])

### add accounts if second argument is passed
if not int(ACCOUNTS):
    print("----- Argument for accounts is not present, not creating any additional accounts --------")
else:
    print(f"---------Creating {ACCOUNTS} accounts-------------")
    for i in range(1, int(ACCOUNTS) + 1):
        subprocess.run([f"{DAEMON}", 'keys', 'add', f"account{i}", '--keyring-backend', 'test', '--home', f"{DAEMON_HOME}-1"])

### ----------Adding genesis accounts--------- ###
print("----------Adding genesis accounts---------")
for i in range(1, int(NODES) + 1):
    if i == 1:
        subprocess.run([f"{DAEMON}", '--home', f"{DAEMON_HOME}-{i}", 'add-genesis-account', f"validator{i}", f"1000000000000{DENOM}", '--keyring-backend', 'test'])
        print(f"done {DAEMON_HOME}-{i} genesis allocation")
        continue
    subprocess.run([f"{DAEMON}", '--home', f"{DAEMON_HOME}-{i}", 'add-genesis-account', f"validator{i}", f"1000000000000{DENOM}", '--keyring-backend', 'test'])
    key_address = check_output([f"{DAEMON}", 'keys', 'show', f"validator{i}", '-a', '--home', f"{DAEMON_HOME}-{i}", '--keyring-backend', 'test'])
    address = key_address.strip().decode()
    subprocess.run([f"{DAEMON}", '--home', f"{DAEMON_HOME}-1", 'add-genesis-account', f"{address}", f"1000000000000{DENOM}"])
print(f"--------Genesis allocation done for {NODES} nodes-----------")

#### "----------Genesis allocation for accounts---------" ####

if not int(ACCOUNTS):
    print("----- Argument for accounts is not present, not creating any additional accounts --------")
else:
    for i in range(1, int(ACCOUNTS) + 1):
        key_address = check_output([f"{DAEMON}", 'keys', 'show', f"account{i}", '-a', '--home', f"{DAEMON_HOME}-1", '--keyring-backend', 'test'])
        address = key_address.strip().decode()
        print(f"cmd ::{DAEMON} --home {DAEMON_HOME}-1 add-genesis-account {address} 1000000000000{DENOM}")
        subprocess.run([f"{DAEMON}", '--home', f"{DAEMON_HOME}-1", 'add-genesis-account', f"{address}", f"1000000000000{DENOM}"])
    print("----------Genesis allocation done for accounts---------")

#### "--------Gentx  creation--------" ####
print("--------Gentx creation--------")
for i in range(1, int(NODES) + 1):
    subprocess.run([f"{DAEMON}", 'gentx', f"validator{i}", f"90000000000{DENOM}", '--chain-id', f"{CHAINID}", '--keyring-backend', 'test', '--home', f"{DAEMON_HOME}-{i}"])

### "---------Copy all gentxs to $DAEMON_HOME-1----------"
print(f"---------Copy all gentxs to {DAEMON_HOME}-1----------")
for i in range(2, int(NODES) + 1):
    source_directory_path = f"{DAEMON_HOME}-{i}/config/gentx"
    destination_directory_path = f"{DAEMON_HOME}-1/config/gentx"
    for source_filename in os.listdir(source_directory_path):
        if source_filename.endswith(".json"):
            source_file_path = os.path.join(source_directory_path, source_filename)
            shutil.copy(source_file_path, destination_directory_path)

### "----------collect-gentxs------------"
subprocess.run([f"{DAEMON}", 'collect-gentxs', '--home', f"{DAEMON_HOME}-1"])

print(f"---------Updating ${DAEMON_HOME}-1 genesis.json ------------")
subprocess.run(['sed', '-i', 's/172800000000000/600000000000/g', f"{DAEMON_HOME}-1/config/genesis.json"])
subprocess.run(['sed', '-i', 's/172800s/600s/g', f"{DAEMON_HOME}-1/config/genesis.json"])
subprocess.run(['sed', '-i', f"s/stake/{DENOM}/g", f"{DAEMON_HOME}-1/config/genesis.json"])

print(f"---------Distribute genesis.json of {DAEMON_HOME}-1 to remaining nodes-------")
for i in range(2, int(NODES) + 1):
    shutil.copy(f"{DAEMON_HOME}-1/config/genesis.json", f"{DAEMON_HOME}-{i}/config/")

print(f"---------Getting public IP address-----------")
r = requests.get('https://ipinfo.io/ip')
IP = r.text

if not IP:
    IP = "127.0.0.1"

print(f"IP : {IP}")
### Setting PERSISTENT_PEERS ###

print("-------Setting PERSISTENT_PEERS---------")
for i in range(1, int(NODES) + 1):
    DIFF = i - 1
    INC = DIFF * 2
    LADDR = 16656 + INC
    print(f"----------Get node-id of {DAEMON_HOME}-{i} ---------")
    encoded_nodeid = check_output([f"{DAEMON}", 'tendermint', 'show-node-id', '--home', f"{DAEMON_HOME}-{i}"])
    nodeID = encoded_nodeid.strip().decode()
    print(f"** Node ID :: {nodeID} **")
    PR=f"{nodeID}@{IP}:{LADDR}"
    if i == 1:
        PERSISTENT_PEERS=f"{PR}"
        continue
    PERSISTENT_PEERS=f"{PERSISTENT_PEERS},{PR}"

###updating config.toml
print("--------updating config.toml----------")
for i in range(1, int(NODES) + 1):
    DIFF = i - 1
    INC = DIFF * 2
    RPC = 16657 + INC
    LADDR = 16656 + INC
    GRPC = 9090 + INC
    WGRPC = 9091 + INC
    print(f"----------Updating {DAEMON_HOME}-{i} chain config-----------")
    subprocess.run(['sed', '-i', f"s#tcp://127.0.0.1:26657#tcp://0.0.0.0:{RPC}#g", f"{DAEMON_HOME}-{i}/config/config.toml"])
    subprocess.run(['sed', '-i', f"s#tcp://0.0.0.0:26656#tcp://0.0.0.0:{LADDR}#g", f"{DAEMON_HOME}-{i}/config/config.toml"])
    subprocess.run(['sed', '-i', f"/persistent_peers =/c\persistent_peers = \"{PERSISTENT_PEERS}\"", f"{DAEMON_HOME}-{i}/config/config.toml"])
    subprocess.run(['sed', '-i', '/allow_duplicate_ip =/callow_duplicate_ip = true',  f"{DAEMON_HOME}-{i}/config/config.toml"])
    subprocess.run(['sed', '-i', '/pprof_laddr =/c\# pprof_laddr = "localhost:6060"',  f"{DAEMON_HOME}-{i}/config/config.toml"])
    subprocess.run(['sed', '-i', f"s#0.0.0.0:9090#0.0.0.0:{GRPC}#g",  f"{DAEMON_HOME}-{i}/config/app.toml"])
    subprocess.run(['sed', '-i', f"s#0.0.0.0:9091#0.0.0.0:{WGRPC}#g",  f"{DAEMON_HOME}-{i}/config/app.toml"])
    subprocess.run(['sed', '-i', '/max_num_inbound_peers =/c\max_num_inbound_peers = 140',  f"{DAEMON_HOME}-{i}/config/config.toml"])
    subprocess.run(['sed', '-i', '/max_num_outbound_peers =/c\max_num_outbound_peers = 110',  f"{DAEMON_HOME}-{i}/config/config.toml"])
print("Updated the configuration files")

### create system services
for i in range(1, int(NODES) + 1):
    DIFF = i - 1
    INC = DIFF * 2
    RPC = 16657 + INC
    print(f"---------Creating /lib/systemd/system/{DAEMON}-{i}.service system file---------")
    service_file = f"""
[Unit]
Description={DAEMON} daemon
After=network.target

[Service]
Environment="DAEMON_HOME={DAEMON_HOME}-{i}"
Environment="DAEMON_NAME={DAEMON}"
Environment="DAEMON_ALLOW_DOWNLOAD_BINARIES=false"
Environment="DAEMON_RESTART_AFTER_UPGRADE=true"
Environment="UNSAFE_SKIP_BACKUP=false"
Type=simple
User={USER}
ExecStart={shutil.which('cosmovisor')} start --home {DAEMON_HOME}-{i}
Restart=on-failure
RestartSec=3
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target"""

    f = open(f"/lib/systemd/system/{DAEMON}-{i}.service", "w+")
    f.write(service_file)
    f.close()
    print(f"-------Starting {DAEMON}-{i} service-------")
    subprocess.run(['sudo', '-S', 'systemctl', 'daemon-reload'])
    subprocess.run(['sudo', '-S', 'systemctl', 'start', f"{DAEMON}-{i}.service"])
    print(f"cmd :: {DAEMON} status --node tcp://localhost:{RPC}")