# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

class UserError(Exception):
    """
    Base class for user management errors
    """
    pass

class UserExists(UserError):
    """
    Represents a user already existing (when trying to add the user).
    """
    pass

class NoSuchUser(UserError):
    """
    Raised when trying to do something to a user that does not exist.
    """
    pass

