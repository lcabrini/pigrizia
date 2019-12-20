# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import time
import re
from getpass import getuser
import shlex
import paramiko
from . import Handler, NoSuchCommand

class RemoteHandler(Handler):
    """
    This is a command handler that executes commands on a remote system
    using Paramiko.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.addr = kwargs['addr']

        if 'passphrase' in kwargs:
            # TODO: is this needed? Since I don't know, I will keep it 
            # here for now.
            self.passphrase = kwargs['passphrase']

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # TODO: check if connection fails
        # TODO: quick fix for now. Think of something better.
        if hasattr(self.passwd)
            self.ssh.connect(self.addr, username=self.user, 
                    password=self.passwd)
        else:
            self.ssh.connect(self.addr, username=self.user)

    def do(self, cmd, **kwargs):
        """
        Invoke a single command as the curent user.

        :param str cmd: the command to run, including arguments
        :return: a tuple consisting of the exit code, output to stdout
            and output to stderr
        :rtype: tuple
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        out = [o.strip() for o in stdout.readlines()]
        err = [e.strip() for e in stderr.readlines()]
        ret = stdout.channel.recv_exit_status()
        if ret == 127:
            raise NoSuchCommand(shlex.split(cmd)[0])
        return ret, out, err

    def sudo(self, cmd, **kwargs):
        """
        Invoke a singled command as another user (by default root).

        :param str cmd: the command to run including the arguments
        :return: a tuple consisting of the exit code, output to stdout
            and output to stderr
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

        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        time.sleep(0.1)
        if passwd is not None:
            stdin.write("{}\n".format(passwd))

        out = [o.strip() for o in stdout.readlines()]
        err = [e.strip() for e in stderr.readlines()]
        if err[0].startswith('[sudo]'):
            err.pop()
        ret = stdout.channel.recv_exit_status()
        return ret, out, err

    def interact(self, script, **kwargs):
        pass
