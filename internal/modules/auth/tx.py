"""This module covers the tx commands of auth CosmosSDK module"""
import os
from internal.utils import exec_command

DAEMON = os.getenv("DAEMON")
HOME = os.getenv("HOME")


def tx_encode(signed_file: str):
    """This function encodes a unsigned transaction file"""
    command = f"{DAEMON} tx encode {HOME}/{signed_file}"
    return exec_command(command)


def tx_decode(encoded_tx):
    """This function decodes an encoded transaction"""
    return exec_command(f"{DAEMON} tx decode {encoded_tx}")
