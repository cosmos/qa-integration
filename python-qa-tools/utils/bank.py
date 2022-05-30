import os, logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

DAEMON = os.getenv('DAEMON')

def print_balance_deductions(wallet, diff):
    if diff > 0:
        logging.info(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        logging.info(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        logging.info(f"No deduction from {wallet} balance")