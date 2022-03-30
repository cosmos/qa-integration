import os
import sys
from dotenv import dotenv_values

### Fetch env values
config = dotenv_values('.env')
DAEMON = config['DAEMON'] if 'DAEMON' in config.keys() and not None else None
DENOM = config['DENOM'] if 'DENOM' in config.keys() and not None else None
CHAINID = config['CHAINID'] if 'CHAINID' in config.keys() and not None else None
DAEMON_HOME = config['DAEMON_HOME'] if 'DAEMON_HOME' in config.keys() and not None else None
GH_URL = config['GH_URL'] if 'GH_URL' in config.keys() and not None else None
CHAIN_VERSION = config['CHAIN_VERSION'] if 'CHAIN_VERSION' in config.keys() and not None else None

def display_usage():
    s = ""
    s += "DAEMON \n" if not DAEMON else ""
    s += "DENOM \n" if not DENOM else ""
    s += "CHAINID \n" if not CHAINID else ""
    s += "DAEMON_HOME \n" if not DAEMON_HOME else ""
    s += "GH_URL \n" if not GH_URL else ""
    s += "CHAIN_VERSION \n" if not CHAIN_VERSION else ""
    
    if not len(s):
        print("** These are the environment variables exported : \n")
        print(f"1. DAEMON = {DAEMON}\n2. DENOM = {DENOM}\n3. CHAINID = {CHAINID}\n4. DAEMON_HOME = {DAEMON_HOME}\n5. GH_URL = {GH_URL}\n6. CHAIN_VERSION = {CHAIN_VERSION}\n")
    else:
        print("** Please export all the necessary env variables in .env file as shown in the .env.example file, These env values are missing:: \n")
        print(s)
    sys.exit()
display_usage()