import subprocess
import shlex

def execute(cmd, workdir):
    """ Get subprocess output"""
    cmd = shlex.split(cmd)
    return subprocess.check_output(cmd, cwd=workdir).decode().strip()