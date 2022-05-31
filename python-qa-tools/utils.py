import argparse, os, json, logging, subprocess

logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

DAEMON = os.getenv('DAEMON')

HOME = os.getenv('HOME')

def print_balance_deductions(wallet, diff):
    if diff > 0:
        logging.info(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        logging.info(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        logging.info(f"No deduction from {wallet} balance")
        

# This function is called for executing commands.
def exec_command(command):
    stdout, stderr = subprocess.Popen(command.split(),
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE).communicate()
    return stdout.strip().decode(), stderr.strip().decode()


def is_tool(binary):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(binary) is not None

def num_txs_type(x):
    if int(x) < 1000:
        raise argparse.ArgumentTypeError('The argument NUM_TXS should be 1000 or more')
    return int(x)

def node_type(x):
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError(f"The number of nodes should be atleast 2, you have entered {x}")
    return x

def create_multi_messages(file_name):
    with open(f"{HOME}/{file_name}", 'r+') as file:
            file_data = json.load(file)
            new_data = file_data["body"]["messages"][-1]
            file_data["body"]["messages"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)