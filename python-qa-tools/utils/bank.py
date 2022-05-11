import os

DAEMON = os.getenv('DAEMON')

def print_balance_deductions(wallet, diff):
    if diff > 0:
        print(f"Balance in the {wallet} increased by {diff}")
    elif diff < 0:
        print(f"Balance in the {wallet} decreased by {-1 * diff}")
    else:
        print(f"No deduction from {wallet} balance")