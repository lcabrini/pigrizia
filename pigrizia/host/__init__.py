# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

class Host:
    """
    A host represents a machine on the network that you can connect to.
    Hosts can be either local or remote and this is determined by the
    existance of the addr key among the keyword arguments.

    This class is a base class for actual hosts. It should never be
    instantiated. Use :func:`~pigrizia.host.detect_host` instead, which
    will return an appropriate host object. (See 
    :class:`~pigrizia.host.linux.Linux` for an example.)
    """

    def __init__(self, **kwargs):
        if 'addr' in kwargs and not kwargs['addr'] is None:
            self.cmdh = ParamikoHandler()
        else:
            self.cmdh = LocalHandler()


def detect_host(addr=None):
    """
    This will detect the host

    :param addr: the IP address or hostname of the host
    :type addr: str or None
    :return: a host object that (hopefully) represents the host at the
        specified address
    :rtype: a subclass of :class:`~pigrizia.host.Host`
    """ 
