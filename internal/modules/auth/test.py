"""
This module contains all auth test functions.
"""
import logging
import time
import unittest
import json

from core.keys import keys_add, keys_show
from modules.auth.query import (
    query_account,
    query_accounts,
    query_params,
)
from internal.modules.bank.query import query_balances
from internal.utils import env
from internal.core.tx import (
    tx_broadcast,
    tx_multi_sign,
    tx_partner_sign,
    tx_sign,
)
from internal.modules.auth.tx import tx_create_vesting_account, tx_decode, tx_encode
from internal.modules.bank.tx import create_unsigned_txs, tx_send


HOME = env.HOME
DEFAULT_GAS = env.DEFAULT_GAS
DENOM = env.DENOM


class TestAuthModuleTxsQueries(unittest.TestCase):
    """
    The class `TestAuthModuleTxsQueries` contains test functions
    which test queries of auth module
    """

    @classmethod
    def setUpClass(cls):
        """
        The function `setUpClass` will be called before running any test case.
        """
        status, multisigaccount = keys_add("multisigaccount", multisig=True)
        assert status, "Failed to add multisig account"
        multi_key_address = multisigaccount["address"]

        status, account1 = keys_show("account1")
        assert status, "Failed to get account1 account details"
        account1_address = account1["address"]

        status, _ = tx_send(
            from_address=account1_address,
            to_address=multi_key_address,
            amount="1000000",
        )
        assert status, "Failed to send coins to multisig account"

        status, _ = keys_add("vestingaccount")
        assert status, "Failed to add vesting account"

    def test_query_account(self):
        """
        The function `test_query_account` will query account
        and test balance
        """
        status, key = keys_show("account1", "acc")
        self.assertTrue(status, key)
        self.assertTrue(key)
        status, query_response = query_account(key["address"])
        self.assertTrue(status, query_response)

    def test_query_accounts(self):
        """
        The function `test_query_accounts` will query accounts
        and test balance
        """
        status, query_response = query_accounts()
        self.assertTrue(status, query_response)

    def test_query_params(self):
        """
        The function `test_query_params` will query params
        and test gas
        """
        status, query_resp = query_params()
        self.assertTrue(status, query_resp)

    def test_tx_encode_and_decode(self):
        """
        The function `test_tx_encode_and_decode` will encode and decode a transaction.
        """
        status, from_account = keys_show("account1", "acc")
        self.assertTrue(status, from_account)
        from_address = from_account["address"]

        status, account_resp = query_account(from_address)
        self.assertTrue(status, account_resp)
        from_address_sequence = account_resp["sequence"]

        status, to_account = keys_show("account2", "acc")
        self.assertTrue(status, to_account)
        to_address = to_account["address"]

        status, unsigned_tx = create_unsigned_txs(
            from_address, to_address, "100stake", "unsigned_tx.json"
        )
        self.assertTrue(status, unsigned_tx)

        status, signed_tx = tx_sign(
            "unsigned_tx.json", from_address, from_address_sequence, DEFAULT_GAS
        )
        self.assertTrue(status, signed_tx)
        with open(HOME + "/" + "signed_tx.json", "w", encoding="utf8") as outfile:
            json.dump(signed_tx, outfile)

        status, encoded_tx = tx_encode("signed_tx.json")
        self.assertTrue(status, encoded_tx)

        status, decoded_json = tx_decode(encoded_tx)
        self.assertTrue(status, decoded_json)
        self.assertEqual(str(signed_tx), str(decoded_json))

    def test_tx_multisign(self):
        """
        test_tx_multisign
        """
        # Fetch multisigaccount, account1 and account2 addresses
        status, multisigaccount = keys_show("multisigaccount")
        self.assertTrue(status, multisigaccount)
        multisig_address = multisigaccount["address"]

        status, account1 = keys_show("account1")
        self.assertTrue(status, account1)
        account1_address = account1["address"]

        status, account2 = keys_show("account2")
        self.assertTrue(status, account2)
        account2_address = account2["address"]

        # make generate-only transaction
        # (Sending amount from multisig_address to account1_address)
        # Storing the transaction result in `unsigned_multisig_tx.json`
        status, multisig_send_tx = tx_send(
            from_address=multisig_address,
            to_address=account1_address,
            amount=5,
            unsigned=True,
        )
        self.assertTrue(status, multisig_send_tx)
        with open(f"{HOME}/unsigned_multisig_tx.json", "w", encoding="utf8") as outfile:
            json.dump(multisig_send_tx, outfile)

        # account1 signing the unsigned_multisig_tx
        # Storing the account1_signtaure in `acc1_signature.json`
        status, acc1_signed_tx = tx_partner_sign(
            "unsigned_multisig_tx.json",
            multisig_address,
            account1_address,
            broadcast_mode="block",
        )
        self.assertTrue(status, acc1_signed_tx)
        with open(f"{HOME}/acc1_signature.json", "w", encoding="utf8") as outfile:
            json.dump(acc1_signed_tx, outfile)

        # account2 signing the unsigned_multisig_tx
        # Storing the account2_signtaure in `acc2_signature.json`
        status, acc2_signed_tx = tx_partner_sign(
            "unsigned_multisig_tx.json",
            multisig_address,
            account2_address,
            broadcast_mode="block",
        )
        self.assertTrue(status, acc2_signed_tx)
        with open(f"{HOME}/acc2_signature.json", "w", encoding="utf8") as outfile:
            json.dump(acc2_signed_tx, outfile)

        # Creating the signed_tx
        signatures_list = ["acc1_signature.json", "acc2_signature.json"]
        status, multisig_signed_tx = tx_multi_sign(
            "unsigned_multisig_tx.json", "multisigaccount", signatures_list
        )
        self.assertTrue(status, multisig_signed_tx)
        with open(f"{HOME}/signed_multisig_tx.json", "w", encoding="utf8") as outfile:
            json.dump(multisig_signed_tx, outfile)

        # Broadcasting the signed tx.
        status, broadcast_resp = tx_broadcast(
            "signed_multisig_tx.json", broadcast_mode="block"
        )
        self.assertTrue(status, broadcast_resp)

    def test_tx_multisign_batch(self):
        # Fetch multisigaccount, account1 and account2 addresses
        status, multisigaccount = keys_show("multisigaccount")
        self.assertTrue(status, multisigaccount)
        multisig_address = multisigaccount["address"]

        status, account1 = keys_show("account1")
        self.assertTrue(status, account1)
        account1_address = account1["address"]

        status, account2 = keys_show("account2")
        self.assertTrue(status, account2)
        account2_address = account2["address"]

        status, unsigned_tx_1 = tx_send(
            from_address=multisig_address,
            to_address=account1_address,
            amount=5,
            unsigned=True,
        )
        self.assertTrue(status, unsigned_tx_1)

        with open(
            f"{HOME}/unsignedmulti_txs_batch.json", "w", encoding="utf8"
        ) as outfile:
            json.dump(unsigned_tx_1, outfile)

        # Get partner signs
        status, acc1_signature = tx_partner_sign(
            "unsignedmulti_txs_batch.json",
            multisig_address,
            account1_address,
            broadcast_mode="block",
            batch=True,
        )
        self.assertTrue(status, acc1_signature)
        with open(f"{HOME}/acc1_signature.json", "w", encoding="utf8") as outfile:
            json.dump(acc1_signature, outfile)

        status, acc2_signature = tx_partner_sign(
            "unsignedmulti_txs_batch.json",
            multisig_address,
            account2_address,
            broadcast_mode="block",
            batch=True,
        )
        self.assertTrue(status, acc2_signature)
        with open(f"{HOME}/acc2_signature.json", "w", encoding="utf8") as outfile:
            json.dump(acc2_signature, outfile)

        signatures = ["acc1_signature.json", "acc2_signature.json"]
        status, signedmulti_txs_batch = tx_multi_sign(
            "unsignedmulti_txs_batch.json", "multisigaccount", signatures, batch=True
        )
        self.assertTrue(status, signedmulti_txs_batch)
        with open(
            f"{HOME}/signedmulti_txs_batch.json", "w", encoding="utf8"
        ) as outfile:
            json.dump(signedmulti_txs_batch, outfile)

        status, broadcast_resp = tx_broadcast(
            "signedmulti_txs_batch.json", broadcast_mode="block"
        )
        self.assertTrue(status, broadcast_resp)

    def test_vesting(self):
        status, vesting_account = keys_show("vestingaccount")
        self.assertTrue(status, vesting_account)

        vesting_address = vesting_account["address"]
        vesting_amount = 10000
        status, create_resp = tx_create_vesting_account(vesting_address, vesting_amount)
        self.assertTrue(status, create_resp)
        logging.info("Creating Vesting Account")
        time.sleep(10)
        status, vesting_account = query_account(vesting_address)
        self.assertTrue(status, vesting_account)
        self.assertEqual(
            vesting_account["@type"],
            "/cosmos.vesting.v1beta1.ContinuousVestingAccount",
            "Error while creating vesting account",
        )
        status, bal_resp = query_balances(vesting_address)
        self.assertTrue(status, bal_resp)
        self.assertEqual(
            str(vesting_amount),
            bal_resp["balances"][0]["amount"],
            "Error while creating vesting account, Mismatched balance",
        )
        # logging.info("Waiting for VestingAccount to become BaseAccount")
        # time.sleep(90)
        # status, vesting_account = query_account(vesting_address)
        # self.assertTrue(status, vesting_account)
        # self.assertEqual(
        #     vesting_account["@type"],
        #     "/cosmos.auth.v1beta1.BaseAccount",
        #     "Error in the Vesting to Base Conversion",
        # )


if __name__ == "__main__":
    logging.info("INFO: running auth module tests")
    unittest.main()
