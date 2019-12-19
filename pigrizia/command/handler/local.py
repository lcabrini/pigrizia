# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import time
from subprocess import Popen, PIPE
import shlex
from . import NoSuchCommand

class LocalHandler:
    """
    This is a command handler the executes commands on the local system.

    """

    def __init__(self, **kwargs):
        pass

    def do(self, cmd, **kwargs):
        """ 
        Run a single command as the current user

        :param str cmd: the command to run, including arguments
        :return: a tuple of return code, stdout, stderr
        :rtype: tuple
        """
        args = shlex.split(cmd)
        try:
            with Popen(args, stdout=PIPE, stderr=PIPE) as p:
                out, err = p.communicate()

            if out:
                out = out.decode().splitlines()
            if err:
                err = err.decode().splitlines()

            return p.returncode, out, err
        except FileNotFoundError as e:
            raise NoSuchCommand(args[0])

    def sudo(self, cmd, **kwargs):
        pass

    def interact(self, script, **kwargs):
        pass

