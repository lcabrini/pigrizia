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
from scp import SCPClient, SCPException
from pigrizia.host import get_host
from . import Handler, NoSuchCommand

class CopyFailed(Exception):
    """
    Inidicates that a copy operation failed.
    """

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
        if hasattr(self, 'passwd'):
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

    def copy(self, src, dest, **kwargs):
        """
        Copies a file.

        :param str src: the file to copy
        :param str dest: the location to copy to.
        :return tuple: the exit code (``int``), stdout (``list``) and 
            stderr (``list``)
        """
        ret, out, err = self.do("mktemp")
        tmp = out[0]
        scp = SCPClient(self.ssh.get_transport())
        try:
            scp.put(src, remote_path=tmp)
        except SCPException as e:
            return 1, [], [e]
        finally:
            scp.close()

        shost = get_host()
        schk = shost.checksum(src)
        cmd = "sha512sum {}".format(tmp)
        if 'sudo' in kwargs and kwargs['sudo'] is True:
            ret, out, err = self.sudo(cmd, **kwargs)
        else:
            ret, out, err = self.do(cmd, **kwargs)
        dchk = out[0].split()[0]
        if schk != dchk:
            raise CopyFailed()
    
        cmd = "cp {} {}".format(tmp, dest)
        if 'sudo' in kwargs and kwargs['sudo'] is True:
            self.sudo(cmd, **kwargs)
        else:
            self.do(cmd, **kwargs)
        # TODO: for now
        return 0, [], []

    def interact(self, script, **kwargs):
        pass
