# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from .config import HostConfig

class Host:
    """
    A host represents a machine on the network that you can connect to.
    Hosts can be either local or remote and this is determined by the
    existance of the addr key among the keyword arguments.

    This class is a base class for actual hosts. It should never be
    instantiated. Use :func:`~pigrizia.host.get_host` instead, which
    will return an appropriate host object. (See 
    :class:`~pigrizia.host.linux.Linux` for an example.)
    """

    _config = None

    def __init__(self, **kwargs):
        if 'addr' in kwargs:
            self._config = HostConfig(kwargs['addr'])
        else:
            self._config = HostConfig()

        if 'addr' in kwargs and kwargs['addr'] is not None:
            from pigrizia.command.handler.remote import RemoteHandler
            self.cmdh = RemoteHandler(**kwargs)
        else:
            from pigrizia.command.handler.local import LocalHandler
            self.cmdh = LocalHandler(**kwargs)

    @property
    def config(self):
        return self._config
