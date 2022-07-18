"""
This module contains all the functions calling keys sub-commands
"""
import os
from internal.utils import exec_command

DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")


# `keys_show` will return the key details in json format.
def keys_show(account, acc_type="acc",home=f"{DAEMON_HOME}-1"):
    """The function `keys_show` will return the key details in json format.

    Args:
        account (_string_): wallet name or bech32 address.
        account_type (str, optional):
        The Bech32 prefix encoding for a key (acc|val|cons) (default "acc").

    Returns:
        _type_: _description_
    """
    command = f"""{DAEMON} keys show {account} --home {home} --bech {acc_type} \
            --keyring-backend test --output json"""
    return exec_command(command)
