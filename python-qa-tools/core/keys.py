"""
This module contains all the functions calling keys sub-commands
"""
import os
import json
from utils import exec_command

DAEMON = os.getenv("DAEMON")
DAEMON_HOME = os.getenv("DAEMON_HOME")


def keys_show(account, account_type="acc"):
    """The function `keys_show` will return the key details in json format.

    Args:
        account (_string_): wallet name or bech32 address.
        account_type (str, optional):
        The Bech32 prefix encoding for a key (acc|val|cons) (default "acc").

    Returns:
        _type_: _description_
    """
    try:
        command = f"""{DAEMON} keys show {account} --home {DAEMON_HOME}-1 --bech {account_type} \
            --keyring-backend test --output json"""
        std_out, std_err = exec_command(command)
        if len(std_err) != 0:
            return False, std_err
        return True, json.loads(std_out)
    except Exception as error:  # pylint: disable=broad-except
        return False, error
