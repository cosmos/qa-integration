"""
This module contains all the functions calling keys sub-commands
"""
from internal.utils import exec_command, env

DAEMON = env.DAEMON
DAEMON_HOME = env.DAEMON_HOME


def keys_add(account: str, multisig=False, home: str = f"{DAEMON_HOME}-1"):
    """The function `keys_add` will add a new key to the keyring.

    Args:
        account (_string_): wallet name or bech32 address.
        home (_string_, optional): home directory of the node (default "{DAEMON_HOME}-1").

    Returns:
        _type_: _description_
    """
    command = f"""{DAEMON} keys add {account} --home {home} --keyring-backend test --output json"""
    if multisig:
        return exec_command(
            command,
            extra_args="--multisig=account1,account2,account3 --multisig-threshold 2",
        )
    return exec_command(command)


# The function `keys_show` will return the key details in json format.
def keys_show(account: str, acc_type: str = "acc", home: str = f"{DAEMON_HOME}-1"):
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


def keys_list(home: str = f"{DAEMON_HOME}-1"):
    """The function `keys_list` will return the key details in json format.

    Args:
        home (_string_, optional): home directory of the node (default "{DAEMON_HOME}-1").

    Returns:
        _type_: _description_
    """
    command = (
        f"""{DAEMON} keys list --home {home} --keyring-backend test --output json"""
    )
    return exec_command(command)
