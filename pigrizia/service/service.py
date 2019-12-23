# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

class Service:
    """
    This represents a service that a host provides. It is up to a subclass
    to define exactly what functions that service provides.
    """

    def __init__(self, host, **kwargs):
        self.host = host
        # For convenience, import the hosts call method.
        self._call = host._call
