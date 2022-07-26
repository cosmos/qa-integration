"""
The Parser class is used for argument parser operations.
"""
import argparse
from internal.modules.auth.query import account_type
from internal.core.keys import keys_show


def get_accounts(sender,receiver,sender_account="validator1"):
    sent_acc, recv_acc = None, None 
    if sender:
        sent_acc = keys_show(sender_account)[1]["address"]
    if receiver:
        recv_acc = keys_show("account2")[1]["address"]
    return sent_acc, recv_acc


class ParseTestsDefaultFlags:  # pylint: disable=R0903
    """
    The ParseTestsDefaultFlags class is used for argument parser operations.
    """

    def __init__(  # pylint: disable=R0913
        self,
        desc,
        sender=False,
        sender_account="account1",
        receiver=False,
    ):
        self.parser = argparse.ArgumentParser(desc)
        self.sender = sender
        self.receiver = receiver
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

    def get_args(self):
        """
        Returns the parsed arguments.
        """
        args = self.parser.parse_args()
        sender = args.sender if self.sender else None
        receiver = args.receiver if self.receiver else None
        return sender, receiver
