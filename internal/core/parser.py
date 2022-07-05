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

    def __init__(  # pylint: disable=R0913
        self,
        desc,
        sender=False,
        sender_account="account1",
        receiver=False,
        num_txs=False,
    ):
        self.parser = argparse.ArgumentParser(desc)
        self.sender = sender
        self.receiver = receiver
        self.num_txs = num_txs
        if self.sender:
            self.parser.add_argument(
                "-s",
                "--sender",
                type=account_type,
                default=keys_show(sender_account)[1]["address"],
                help="Sender bech32 address",
            )
        if self.receiver:
            self.parser.add_argument(
                "-r",
                "--receiver",
                type=account_type,
                default=keys_show("account2")[1]["address"],
                help="Receiver bech32 address",
            )
        if self.num_txs:
            self.parser.add_argument(
                "-n",
                "--num_txs",
                type=validate_num_txs,
                default=10000,
                help="Number of transactions to be made, should be positive integer",
            )

    def get_args(self):
        """
        Returns the parsed arguments.
        """
        args = self.parser.parse_args()
        sender = args.sender if self.sender else None
        receiver = args.receiver if self.receiver else None
        num_txs = int(args.num_txs) if self.num_txs else None
        return sender, receiver, num_txs
