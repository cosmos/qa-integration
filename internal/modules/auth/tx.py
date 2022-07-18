from internal.utils import exec_command


import os

DAEMON = os.getenv("DEAMON")
HOME = os.getenv("HOME")


def tx_encode(signed_file):
    return exec_command(f"{DAEMON} tx encode {HOME}/{signed_file}")


def tx_decode(encoded_tx):
    return exec_command(f"{DAEMON} tx decode {encoded_tx}")
