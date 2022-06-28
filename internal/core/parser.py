"""
The Parser class is used for argument parser operations.
"""
import argparse
from internal.modules.auth.query import account_type
from internal.core.keys import keys_show
from internal.utils import validate_num_txs


class Parser:  # pylint: disable=R0903
    """
    The Parser class is used for argument parser operations.
    """

    def __init__(self, desc, sender=False, receiver=False, num_txs=False):
        self.parser = argparse.ArgumentParser(desc)
        if sender:
            self.parser.add_argument(
                "-s",
                "--sender",
                type=account_type,
                default=keys_show("account1")[1]["address"],
                help="Sender bech32 address",
            )
        if receiver:
            self.parser.add_argument(
                "-r",
                "--receiver",
                type=account_type,
                default=keys_show("account2")[1]["address"],
                help="Receiver bech32 address",
            )
        if num_txs:
            self.parser.add_argument(
                "-n",
                "--num_txs",
                type=validate_num_txs,
                default=10000,
                help="Number of transactions to be made, should be positive integer",
            )
