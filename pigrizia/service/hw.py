# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from . import System

class Hardware(System):
    """
    This class represents the host's hardware.
    """
    
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

