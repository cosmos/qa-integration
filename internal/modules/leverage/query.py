"""
Querying functions for the leverage module.
"""

from internal.utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC


def query_registered_tokens():
    command = f"{DAEMON} q leverage registered-tokens --node {RPC} --output json"
    return exec_command(command)
