"""
This module contains all env variables.
"""
import os

DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")
DENOM = os.getenv("DENOM")
CHAINID = os.getenv("CHAINID")
HOME = os.getenv("HOME")
RPC = os.getenv("RPC")
NUM_TXS = int(os.getenv("NUM_TXS", "50"))
NUM_MSGS = int(os.getenv("NUM_MSGS", "30"))
URI = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "qa_test")
TEST_TYPE = os.getenv("TEST_TYPE", None)
DEFAULT_GAS = int(os.getenv("DEFAULT_GAS", "2000000"))

def get(env_var):
    return os.getenv(env_var)
