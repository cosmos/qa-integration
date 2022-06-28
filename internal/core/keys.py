"""
This module contains all the functions calling keys sub-commands
"""
import os
from internal.utils import process_response

DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")


def keys_show(account, acc_type="acc"):
    """The function `keys_show` will return the key details in json format.

    Args:
        account (_string_): wallet name or bech32 address.
        account_type (str, optional):
        The Bech32 prefix encoding for a key (acc|val|cons) (default "acc").

    Returns:
        _type_: _description_
    """
    command = f"""{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --bech {acc_type} \
            --keyring-backend test --output json"""
    return process_response(command)
