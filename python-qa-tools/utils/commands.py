import subprocess

def command_processor(command):
    stdout, stderr = subprocess.Popen(command.split(),
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE).communicate()
    return stdout.strip().decode(), stderr.strip().decode()


def is_tool(binary):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(binary) is not None