import os, json

from utils import exec_command

DAEMON = os.getenv('DAEMON')
RPC = os.getenv('RPC')

def query_balances(address):
    try:
        command = f"{DAEMON} q bank balances {address} --node {RPC} --output json"
        balance, balanceerr = exec_command(command)
        if len(balanceerr):
            return False, balanceerr
        return True, json.loads(balance)
    except Exception as e:
        return False, e
    
# def validate_balances(address, expected_balance):
#     try:
#         status, balance_response = query_balances(address)
#         if not status:
#             return status, balance_response
#         balance_response = json.loads(balance_response)
#         current_balance = int(balance_response['balances'][0]['amount'])
#         if current_balance == int(expected_balance):
#             return True, "Expected and Original balances are equal"
#         return False, "Expected and Original balances does not match"
        
#     except Exception as e:
#         return False, e