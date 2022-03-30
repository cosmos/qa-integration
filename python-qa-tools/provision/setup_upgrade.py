import argparse, os, subprocess, sys, shutil
from dotenv import dotenv_values
from utils.types import node_type

### Fetch env values
config = dotenv_values('.env')
DAEMON = config['DAEMON']
DENOM = config['DENOM']
CHAINID = config['CHAINID']
DAEMON_HOME = config['DAEMON_HOME']
GH_URL = config['GH_URL']
CHAIN_VERSION = config['CHAIN_VERSION']
UPGRADE_NAME = config['UPGRADE_NAME']
UPGRADE_VERSION = config['UPGRADE_VERSION']
HOME = os.getenv('HOME')

parser = argparse.ArgumentParser(description='This program takes inputs for intializing nodes configuration.')
parser.add_argument('nodes', type= node_type, help= 'Number of nodes to be upgraded. Min. 2 should be given')
args = parser.parse_args()
print(f" ** Number of nodes : {args.nodes} to be upgraded **") 
NODES = str(args.nodes)
os.chdir(os.path.expanduser('~'))

### Build the upgrade version
if not GH_URL:
    sys.exit('The environment varible \'GH_URL\' is None make sure to update the env values in .env file')

REPO = GH_URL.split('/')[-1]
shutil.rmtree(REPO)

git = {
    'clone' : f"git clone {GH_URL}",
    'fetch' : 'git fetch',
    'checkout' : f"git checkout {UPGRADE_VERSION}",
    'build' : "make build"
}
subprocess.run(git['clone'].split())
os.chdir(REPO)
subprocess.run(git['fetch'].split())
subprocess.run(git['checkout'].split())
subprocess.run(git['build'].split())

for i in range(1, int(NODES) + 1):
    os.environ[f'{DAEMON_HOME}_{i}'] = f"{DAEMON_HOME}-{i}"
    try:
        os.makedirs(f"{DAEMON_HOME}-{i}/cosmovisor/upgrades/{UPGRADE_NAME}/bin")
    except FileExistsError as e:
        print(f"The path '{DAEMON_HOME}-{i}/cosmovisor/upgrades/{UPGRADE_NAME}/bin' already exists, skipping the creation.")
    shutil.copy(f"{HOME}/{REPO}/build/{DAEMON}", f"{DAEMON_HOME}-{i}/cosmovisor/upgrades/{UPGRADE_NAME}/bin/")

print("-------- New upgraded binary is moved to cosmovisor ---------")