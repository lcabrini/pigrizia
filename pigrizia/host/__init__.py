# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os

import logging
logger = logging.getLogger()
from .config import get_host_config

class UnknownSystem(Exception):
    """
    Raised if the system cannot be detected
    """
    pass

def get_host(**kwargs):
    """
    Gets a host.

    :return: a host object that (hopefully) represents the host at the
        specified address
    :rtype: a subclass of :class:`~pigrizia.host.Host`
    """
    # TODO: this function has to be rewritten, because it is really clumsy.
    # for now it get the job done, however.
    from .linux import (Fedora, Issabel, CentOS, Ubuntu, Proxmox, 
            Debian, Linux)

    if 'addr' not in kwargs and 'label' in kwargs:
        host_config = get_host_config(kwargs['label'])
        if 'addr' in host_config:
            kwargs['addr'] = host_config['addr']
        else:
            # TODO: is this the right error?
            raise KeyError("unknown host: {}".format(kwargs['label']))

    linux = Linux(**kwargs)
    if Fedora.detect(linux):
        logger.info("detected Fedora")
        return Fedora(**kwargs)
    elif Issabel.detect(linux):
        logger.info("detected Issabel")
        return Issabel(**kwargs)
    elif CentOS.detect(linux):
        logger.info("detected CentOS")
        return CentOS(**kwargs)
    elif Ubuntu.detect(linux):
        logger.info("detected Ubuntu")
        return Ubuntu(**kwargs)
    elif Proxmox.detect(linux):
        return Proxmox(**kwargs)
    elif Debian.detect(linux):
        logger.info("detected debian")
        return Debian(**kwargs)
    elif linux.uname == 'Linux':
        return linux
    else:
        # We really don't know how the system works, so better just raise
        # an exception.
        raise UnknownSystem()
