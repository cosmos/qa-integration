"""
This module has functions to store stats in mongodb
"""
import json
import logging
import utils
from internal.db import db

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

COL_NAME = "test_stats"
TX_TYPE = "tx"
QUERY_TYPE = "query"


def insert_stat(data):
    """
    This function will store the test results in DB.
    Args:
        data (_dict_): _Test data_
    """
    _ = db[COL_NAME].insert_one(data)


def record_stat(test_type, cmd_type, output, err):
    """
    This function parses the transctin response and stores in DB
    Args:
        test_type (_str_): _str_
        cmd_type (_str_): _str_
        output (_str_ | dict): _dict_ | _str_
        err (_str_): _bool_
    """
    if err:
        logging.error("ERROR: %s", err)
        stat = {
            "test_type": test_type,
            "cmd_type": cmd_type,
            "success": False,
            "code": "unknown",
            "error_type": "unknown",
            "error": err,
        }
        insert_stat(stat)
        return
    out = (
        json.loads(output)
        if output[0] == "{" or output[0] == "["
        else {"code": 0, "txhash": output}
    )
    if isinstance(out, dict) and "code" in out:
        if out["code"] != 0:
            logging.error("ERROR: %s", out)
            error_type = out["raw_log"]
            split_raw_log = error_type.split(":")
            if len(split_raw_log) > 0:
                error_type = split_raw_log[-1].strip()
            stat = {
                "test_type": test_type,
                "cmd_type": cmd_type,
                "success": False,
                "code": out["code"],
                "error_type": error_type,
                "error": out["raw_log"],
                "txhash": out["txhash"],
            }
        else:
            stat = {
                "test_type": test_type,
                "cmd_type": cmd_type,
                "success": True,
                "code": out["code"],
                "txhash": out["txhash"],
            }
    elif test_type is not None and cmd_type == "query":
        stat = {
            "test_type": test_type,
            "cmd_type": cmd_type,
            "success": True,
        }
    else:
        stat = None

    if stat:
        insert_stat(stat)


def clear_data_by_type():
    """
    Clears the DB data by given test type
    """
    if utils.env.TEST_TYPE:
        db[COL_NAME].delete_many({"test_type": utils.env.TEST_TYPE})


def print_stats(cmd_type=TX_TYPE):
    """
    This function prints the stats from DB.
    """
    test_type = utils.env.TEST_TYPE
    if test_type:
        log_text = "transactions" if cmd_type == TX_TYPE else "queries"
        num_txs = db[COL_NAME].count_documents(
            {"test_type": test_type, "cmd_type": cmd_type}
        )

        num_success_txs = db[COL_NAME].count_documents(
            {"test_type": test_type, "cmd_type": cmd_type, "success": True}
        )

        num_failed_txs = db[COL_NAME].count_documents(
            {"test_type": test_type, "cmd_type": cmd_type, "success": False}
        )

        num_success_txs_percentage = (
            f"({(num_success_txs/num_txs)*100}%)" if num_txs != 0 else ""
        )
        num_failed_txs_percentage = (
            f"({(num_failed_txs/num_txs)*100}%)" if num_txs != 0 else ""
        )
        stats_log = f"""
Testing stats of {test_type} tests:
-----------------------------
Number of {log_text} executed: {num_txs}
Number of successful {log_text}: {num_success_txs} {num_success_txs_percentage}
Number of failed {log_text}: {num_failed_txs} {num_failed_txs_percentage}\n
"""
        if num_failed_txs and cmd_type == TX_TYPE:
            stats_log += "Failures:\n"
            failures = list(
                db[COL_NAME].aggregate(
                    [
                        {
                            "$match": {
                                "test_type": test_type,
                                "cmd_type": cmd_type,
                                "success": False,
                            }
                        },
                        {
                            "$group": {
                                "_id": "$code",
                                "count": {"$count": {}},
                                "items": {"$push": "$$ROOT"},
                            }
                        },
                    ]
                )
            )
            for item in failures:
                if item["_id"] == "unknown":
                    stats_log += f"Runtime errors: {item['count']}\n"
                else:
                    stats_log += f"""Failed with code {item['_id']} \
                    ({item['items'][0]['error_type']}): {item['count']}\n"""

        stats_log += "-----------------------------"
        logging.info(stats_log)
        with open("stats.txt", "w", encoding="utf8") as file:
            file.write(stats_log)
            file.close()
