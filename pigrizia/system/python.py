# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from . import System

class Python(System):
    """
    This subsystem represents Python and related tools (such as pip).
    """

    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    def version(self, **kwargs):
        """
        Gets the python version.
        """
        return "{}.{}".format(self._major_version(), self._minor_version())

    def _major_version(self, **kwargs):
        cmd = "python -c 'import sys; print(sys.version_info.major)'"
        ret, out, err = self._call(cmd, **kwargs)
        return out[0]

    def _minor_version(self, **kwargs):
        cmd = "python -c 'import sys; print(sys.version_info.minor)'"
        ret, out, err = self._call(cmd, **kwargs)
        return out[0]
