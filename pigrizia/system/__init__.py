# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

class System:
    """
    This represents a subsystem on a host (strange then that it called
    a system, but that is just one of those things). It is up to 
    subclasses to define particular subsystems.

    System classes mainly exist to break the functionilty of a host
    into smaller, more manageable parts.
    """

    def __init__(self, host, **kwargs):
        self.host = host
        # For convenience, import the hosts call method.
        self._call = host._call
