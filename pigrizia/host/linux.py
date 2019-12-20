# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import logging
from . import Host

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

    def whoami(self, **kwargs):
        """
        Gets the name of the current user.

        :returns: the name of the current user
        :rtype: str
        """
        ret, out, err = self._call("whoami", **kwargs)
        return out[0]

    def _call(self, cmd, **kwargs):
        if 'sudo' in kwargs and kwargs['sudo'] is True:
            return self.cmdh.sudo(cmd)
        else:
            return self.cmdh.do(cmd)

    def __str__(self):
        return "Linux"
