import argparse, os, json, logging, subprocess

from stats import check_status

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

DAEMON = os.getenv("DAEMON")

HOME = os.getenv("HOME")

# The function `print_balance_deductions` will print information about the balance deductions after transactions for a wallet or account.
def print_balance_deductions(wallet, diff):
    if diff > 0:
        logging.error("Some of the transactions failed")
        logging.info(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        logging.error("Some of the transactions failed")
        logging.info(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        logging.info(
            f"All transaction went successfully, No deduction from {wallet} balance"
        )


# The utility function `exec_command` is used to execute the cosmos-sdk based commands.
def exec_command(command, test_type=None, cmd_type=None):
    try:
        stdout, stderr = subprocess.Popen(
            command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        out, err = stdout.strip().decode(), stderr.strip().decode()
        if test_type:
            check_status(test_type, cmd_type, out, err)
        return out, err
    except Exception as e:
        if test_type:
            check_status(test_type, cmd_type, '', e)
        return None, e


# The utility function `is_tool` is used to verify the package or binary installation.
def is_tool(binary):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(binary) is not None


# validate_num_txs will validate num_txs value
def validate_num_txs(x):
    if int(x) < 1:
        raise argparse.ArgumentTypeError(
            "The argument NUM_TXS should be positive integer"
        )
    return int(x)


# node_type is a user-defined type.
def node_type(x):
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError(
            f"The number of nodes should be atleast 2, you have entered {x}"
        )
    return x


# The function `create_multi_messages` is used to duplicate the messages in a single transaction.
def create_multi_messages(num_msgs, file_name):
    messages = []
    with open(f"{HOME}/{file_name}", "r+") as file:
        file_data = json.load(file)
        messages.append(file_data["body"]["messages"][-1])
    for i in range(num_msgs):
        messages.append(messages[-1])

    with open(f"{HOME}/{file_name}", "r+") as file:
        file_data = json.load(file)
        file_data["body"]["messages"] = messages
        file.seek(0)
        json.dump(file_data, file, indent=4)


# check_tx_result checks tx whether failed or success and update count based on it
def check_tx_result(
    tx_result,
    status,
    failed_code_errors,
    num_success_txs,
    num_failed_txs,
    num_other_errors,
):
    if not status:
        num_failed_txs += 1
        logging.error(f"ERROR: {tx_result}")
        if type(tx_result) is dict and "code" in tx_result:
            if tx_result["code"] not in failed_code_errors:
                failed_code_errors[tx_result["code"]] = []
            error_type = tx_result["raw_log"]
            split_raw_log = error_type.split(":")
            if len(split_raw_log):
                error_type = split_raw_log[-1].strip()

            failed_code_errors[tx_result["code"]].append(error_type)
        else:
            num_other_errors += 1

    else:
        num_success_txs += 1

    return failed_code_errors, num_success_txs, num_failed_txs, num_other_errors


def print_tx_summary(
    num_txs,
    num_msgs,
    failed_code_errors,
    num_success_txs,
    num_failed_txs,
    num_other_errors,
):
    logging.info(
        f"""
Testing Stats:
-----------------------------
Number of transactions executed: {num_txs}
Number of messages executed: {num_msgs}
Number of successful transactions: {num_success_txs} ({(num_success_txs/num_txs)*100}%)
Number of failed transactions: {num_failed_txs} ({(num_failed_txs/num_txs)*100}%)
        """
    )
    if num_failed_txs:
        logging.info("Failures:")
        for key, value in failed_code_errors.items():
            logging.info(f"Failed with code {key} ({value[0]}): {len(value)}")
        if num_other_errors:
            logging.info(f"Other errors: {num_other_errors}")

    logging.info("-----------------------------")
