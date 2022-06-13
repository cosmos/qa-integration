import json
from db import db

COL_NAME = "test_stats"


def insert_stat(data):
    _ = db[COL_NAME].insert_one(data)


def check_status(test_type, cmd_type, output, err):
    if err:
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

    out = json.loads(output)
    if type(out) is dict and "code" in out:
        if out["code"] != 0:
            error_type = out["raw_log"]
            split_raw_log = error_type.split(":")
            if len(split_raw_log):
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


def clear_data_by_type(test_type):
    db[COL_NAME].delete_many({"test_type": test_type})


def print_stats(test_type, cmd_type):
    stats = list(db[COL_NAME].find({"test_type": test_type, "cmd_type": cmd_type}))
    return stats
