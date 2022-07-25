"""_summary_
The functions in this module calls Bank transaction subcommands.
"""
import json
from internal.core.tx import tx_broadcast, tx_sign
from internal.utils import exec_command, env

DAEMON = env.DAEMON
DENOM = env.DENOM
CHAINID = env.CHAINID
HOME = env.HOME
DAEMON_HOME = env.DAEMON_HOME
RPC = env.RPC
DEFAULT_GAS = env.DEFAULT_GAS

def create_unsigned_txs(from_address, to_address, amount, file_name):
    """
    The function 'create_unsigned_txs' takes sender(from_address), receiver(to_address), amount
    and file_name as parameters and call the function tx_send internally and stores the json to
    file_name file.

    Args:
        from_address (_str_): sender bech32 address
        to_address (_str_): receiver bech32 address
        amount (_unit_): amount to be transferred
        file_name (_str_): filepath to store unsigned transactions

    Returns:
        _tuple_: (bool, str|json)
    """
    try:
        status, unsigned_tx = tx_send(
            from_address, to_address, amount, gas=DEFAULT_GAS, unsigned=True
        )
        if not status:
            return status, unsigned_tx
        with open(HOME + "/" + file_name, "w", encoding="utf8") as outfile:
            json.dump(unsigned_tx, outfile)
        return True, unsigned_tx
    except Exception as error:  # pylint: disable=broad-except
        return False, error


def sign_and_broadcast_txs(unsigned_file, signed_file, from_address, sequence):
    """
    The function 'sign_and_broadcast_txs' takes unsigned_file, signed_file, from_address
    and sequence as parameters.
    Signs and the broadcasts the unsigned transactions.
    Args:
        unsigned_file (_str_): file path to fetch unsigned transactions.
        signed_file (_str_): filepath to write signed transactions.
        from_address (_type_): sender bech address
        sequence (_type_): The sequence number of the signing account (offline mode only).

    Returns:
        _tuple_: (bool, str|json)
    """
    try:
        status, sign_tx = tx_sign(unsigned_file, from_address, sequence, DEFAULT_GAS)
        if not status:
            return status, sign_tx
        with open(HOME + "/" + signed_file, "w", encoding="utf8") as outfile:
            json.dump(sign_tx, outfile)

        status, broadcast_response = tx_broadcast(signed_file, DEFAULT_GAS, "block")
        if not status:
            return status, broadcast_response
        return status, broadcast_response["txhash"]
    except Exception as error:  # pylint: disable=broad-except
        return False, error


# tx_send takes from_address, to_address and amount as paramaters and
# internally calls the 'tx send' command and return the response in json format.
def tx_send(  # pylint: disable=C0330, R0913
    from_address,
    to_address,
    amount,
    gas=DEFAULT_GAS,
    unsigned=False,
    sequence=None,
):
    """
    The function tx_send internally calls the 'tx send' command
    and return the response in json format.
    Args:
        from_address (_str_): sender bech address
        to_address (_str_): receiver bech address
        amount (_uint_): amount to be transferred.
        gas (str, optional): gas limit to set per-transaction; set to "auto"
        to calculate sufficient gas automatically (default auto).
        unsigned (bool, optional): Defaults to False.
        sequence (_uint_, optional): The sequence number of the signing account (offline mode only)
        defaults to None.

    Returns:
        _tuple_: bool, str|json
    """
    if unsigned:
        command = f"""{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} \
            --chain-id {CHAINID} --output json --node {RPC} --generate-only --gas {gas}"""
    else:
        if sequence is not None:
            command = f"""{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} \
                --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} \
                    --output json -y --sequence {sequence} --gas {gas}"""

        else:
            command = f"""{DAEMON} tx bank send {from_address} {to_address} {amount}{DENOM} \
                --chain-id {CHAINID} --keyring-backend test --home {DAEMON_HOME}-1 --node {RPC} \
                    --output json -y --gas {gas}"""
    return exec_command(command)
