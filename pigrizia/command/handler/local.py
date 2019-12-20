# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import time
from subprocess import Popen, PIPE
import pexpect
import shlex
from . import NoSuchCommand, BadPassword

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
        """
        Invoke a single command as the specified user (the default is
        root).

        :param str cmd: the command-line to execute.
        :return: a tuple consisting of the exit code of the command,
            stdout and stderr
        :rtype: tuple
        """

        if 'user' in kwargs:
            cmd = "sudo -Su {} {}".format(kwargs['user'], cmd)
        else:
            cmd = "sudo -S {}".format(cmd)

        if 'passwd' in kwargs:
            passwd = kwargs['passwd']
        elif hasattr(self, 'passwd'):
            passwd = self.passwd
        else:
            passwd = None
    
        args = shlex.split(cmd)
        with Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE) as p:
            if passwd is not None:
                passwd = "{}\n".format(passwd).encode()
                out, err = p.communicate(passwd)
            else:
                out, err = p.communicate()

        out = out.decode().splitlines() if out else []
        err = err.decode().splitlines() if err else []
        return p.returncode, out, err

    def interact(self, script, **kwargs):
        pass
