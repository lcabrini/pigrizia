import time
from subprocess import Popen, PIPE
import shlex

class LocalHandler:
    """
    This is a command-handler the executes commands on the local system.

    """

    def __init__(self, **kwargs):
        pass

    def do(self, cmd, **kwargs):
        pass

    def sudo(self, cmd, **kwargs):
        pass

    def interact(self, script, **kwargs):
        pass

