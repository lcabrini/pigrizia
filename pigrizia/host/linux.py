# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import logging
import string
import secrets
import crypt
from . import Host, UserExists, NoSuchUser

logger = logging.getLogger(__name__)

class Linux(Host):
    """
    This represents a system running some form of Linux.

    Keyword Arguments
    -----------------

    There are a few keyword arguments that can be passed in to command
    methods.

    * *sudo* (`bool`): if True the command will be run using sudo. The
        default is False.
    * *pty* (`bool`): if True then the command will be run in a pty. The
        default is False.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def directory_exists(self, path, **kwargs):
        """ 
        Checks if the specified path exists and is a directory.

        :param str path: the path to check for
        :returns: True if path is a directory or False if it isn't
        :rtype: bool
        """
        cmd = "test -d {}".format(path)
        ret, out, err = self._call(cmd, **kwargs)
        return ret == 0

    def file_exists(self, path, **kwargs):
        """
        Checks if the specified path exists and is a file.

        :param str path: the path to check for
        :returns: True if the path is a file or False if it isn't
        :rtype: bool
        """
        cmd = "test -f {}".format(path)
        ret, out, err = self._call(cmd, **kwargs)
        return ret == 0

    def mkdir(self, path, **kwargs):
        """
        Creates the specified directory.
        """
        cmd = "mkdir -p {}".format(path)
        ret, out, err = self._call(cmd, **kwargs)
        return ret

    def rmdir(self, path, **kwargs):
        """
        Removes the specified directory.
        """
        if 'recursive' in kwargs:
            cmd = "rm -rf {}".format(path)
        else:
            cmd = "rmdir {}".format(path)
        ret, out, err = self._call(cmd, **kwargs)
        return ret

    def whoami(self, **kwargs):
        """
        Gets the name of the current user.

        :returns: the name of the current user
        :rtype: str
        """
        ret, out, err = self._call("whoami", **kwargs)
        return out[0] if len(out) > 0 else ''

    def useradd(self, user, **kwargs):
        """
        Adds a user to this system.

        :param str user: the name of the user to add
        :param str passwd: the encrypted password
        :return: True if the user was created, otherwise False
        :rtype: bool
        """
        if self.user_exists(user):
            raise UserExists(user)

        cmd = "useradd"

        if 'create_home' in kwargs and kwargs['create_home'] == False:
            pass
        else:
            cmd += " -m"

        if 'passwd' in kwargs:
            passwd = kwargs['passwd']
        else:
            passwd = self._gen_password()
        passwd = self._crypt(passwd)

        # TODO: if the password above was generated, then the only 
        # reference to it is this one local variable. We better do
        # something with that password or it will get lost forever.

        cmd += ' -p {}'.format(passwd)
        cmd += ' {}'.format(user)
        kwargs['sudo'] = True
        ret, out, err = self._call(cmd, **kwargs)
        return ret == 0

    def userdel(self, user, **kwargs):
        """
        Removes a user from the current system
        
        :param str user: the user to delete
        :return: True if the user was deleted, otherwise False
        :rtype: bool
        """
        if not self.user_exists(user):
            raise NoSuchUser(user)

        cmd = 'userdel -r {}'.format(user)
        kwargs['sudo'] = True
        ret, out, err = self._call(cmd, **kwargs)
        return ret == 0

    def user_exists(self, user, **kwargs):
        """
        Checks if a user exists on the current system.

        :param str user: the user to check for
        :return: True if the user exists or False if they don't
        :rtype: bool
        """
        cmd = "cat /etc/passwd"
        ret, out, err = self._call(cmd, **kwargs)
        for line in out:
            if line.startswith("{}:".format(user)):
                return True
        return False

    def uname(self, **kwargs):
        """
        Returns the uname

        :return: the kernel name
        :rtype: str
        """
        ret, out, err = self_call("uname")
        return ret[0]

    def distro(self, **kwargs):
        """
        Reads the ID of the current distro.

        :return: the value of the ID field of /etc/os-release, or None
            if the file does not exist
        :rtype: str or NoneType
        """
        if not self.file_exists('/etc/os-release'):
            return None

        cmd = "cat /etc/os-release"
        ret, out, err = self._call(cmd, **kwargs)
        for line in out:
            if line.startswith("ID="):
                return line.split('=')[1] 
        # Hopefully we don't get here, but ...
        return None

    def _call(self, cmd, **kwargs):
        if 'sudo' in kwargs and kwargs['sudo'] is True:
            return self.cmdh.sudo(cmd)
        else:
            return self.cmdh.do(cmd)

    def _gen_password(self):
        alpha = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alpha) for i in range(12))

    def _crypt(self, passwd):
        return crypt.crypt(passwd, crypt.mksalt())

    def __str__(self):
        return "Linux"

class Fedora(Linux):
    """
    This represents Fedora Linux.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.package_sets = {}

    @staticmethod
    def detect(host):
        return host.distro() == 'fedora'

class CentOS(Linux):
    """
    Representation of CentOS.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.package_sets = {}

    @staticmethod
    def detect(host):
        return host.distro() == 'centos'

class Issabel(CentOS):
    """
    Represents Issabel.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def backup(self, **kwargs):
        """

        """
        pass

    @staticmethod
    def detect(host):
        # ID in /etc/os-release is centos, not issabel.
        return host.file_exists('/etc/issabel.conf')

class Debian(Linux):
    """
    Representation of Debian GNU/Linux.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.package_sets = {}

    @staticmethod
    def detect(host):
        return host.distro() == 'debian'

class Ubuntu(Debian):
    """
    Represents Ubuntu.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def detect(host):
        return host.distro() == 'ubuntu'

class Proxmox(Debian):
    """
    Representation of Proxmox.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def detect(host):
        return host.distro() and host.directory_exists('/etc/pve')
