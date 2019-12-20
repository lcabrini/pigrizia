# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from getpass import getuser

class NoSuchCommand(Exception):
    """
    Represents a command that cannot be found.
    """
    pass

class Handler:
    """ 
    Base class for command handlers. Don't instantiate this.
    """

    def __init__(self, **kwargs):
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

