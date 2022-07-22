from internal.utils import exec_command, env

DAEMON = env.DAEMON
RPC = env.RPC
CHAINID = env.CHAINID

# 'query_module_version' quereis the respective module's consensus versions..
def query_module_version(module_name):
    command = (
        f"{DAEMON} q upgarde module_versions {module_name} --node {RPC} --output json"
    )
    return exec_command(command)

# 'query_module_versions' quereis all the module's consensus versions..
def query_module_versions(module_name):
    command = (
        f"{DAEMON} q upgarde module_versions {module_name} --node {RPC} --output json"
    )
    return exec_command(command)
