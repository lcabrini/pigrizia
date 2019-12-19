# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from getpass import getuser
import paramiko
from . import NoSuchCommand

class RemoteHandler:
    """
    This is a command handler that executes commands on a remote system
    using Paramiko.
    """

    def __init__(self, **kwargs):
        self.addr = kwargs['addr']

        if 'user' in kwargs:
            self.user = kwargs['user']
        else:
            self.user = getuser()

        if 'passwd' in kwargs:
            self.passwd = kwargs['passwd']
        else:
            # For now we don't do anything, since it is fully possible
            # that the user doesn't need a password (key-based SSH). But
            # we'll keep the else here since I am sure to have forgot
            # something.
            pass

        if 'passphrase' in kwargs:
            # TODO: is this needed? Since I don't know, I will keep it 
            # here for now.
            self.passphrase = kwargs['passphrase']

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # TODO: check if connection fails
        self.ssh.connect(self.addr, username=self.user, 
                password=self.passwd)

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
            raise NoSuchCommand(cmd)
        return ret, out, err

    def sudo(self, cmd, **kwargs):
        pass

    def interact(self, script, **kwargs):
        pass
