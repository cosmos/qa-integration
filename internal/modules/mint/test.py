import logging,time,json
from core.keys import keys_show
from modules.mint.query import *

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

HOME = os.getenv("HOME")
DAEMON_HOME = os.getenv("DAEMON_HOME")

logging.info("INFO :: Running mint module test scripts")


def test_params_query():
     # query params
    path = f"{HOME}/.simd-1/config/"
    with open(path+'genesis.json') as file:
        data = json.load(file)

    query_param = query_params()[1]

    if data["app_state"]["mint"]["params"] == query_param:
        logging.info("querying params was successful")
    else:
        logging.error("missmatch in params")
    time.sleep(5)

def test_inflation_query():
    inflation = query_inflation()[1]
    if inflation:
        logging.info("Querying minting inflation successful")
    else:
        logging.info("Querying minting inflation was failed")
    time.sleep(5)

def test_annual_provision_query():
    provision = query_annual_provision()[1]
    if provision:
        logging.info("Querying minting annual provision successful")
    else:
        logging.info("Querying minting annual provision was failed")
    time.sleep(5)


test_params_query()
test_inflation_query()
test_annual_provision_query()
