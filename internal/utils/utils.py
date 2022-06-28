import argparse, json, logging, subprocess

import utils.env as env

from stats import record_stat, TX_TYPE, QUERY_TYPE

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

HOME = env.HOME

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
def exec_command(command):
    try:
        test_type = env.TEST_TYPE
        # getting command type
        sub_commands = command.split()
        cmd_type = None
        if len(sub_commands) > 1 and (
            sub_commands[1] == "q" or sub_commands[1] == "query"
        ):
            cmd_type = QUERY_TYPE
        elif len(sub_commands) > 1 and (sub_commands[1] == "tx"):
            cmd_type = TX_TYPE

        stdout, stderr = subprocess.Popen(
            command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        out, err = stdout.strip().decode(), stderr.strip().decode()
        if test_type and cmd_type:
            record_stat(test_type, cmd_type, out, err)
        return out, err
    except Exception as e:
        if test_type and cmd_type:
            record_stat(test_type, cmd_type, "", e)
        return None, e


# The utility function `is_tool` is used to verify the package or binary installation.
def is_tool(binary):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(binary) is not None


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
