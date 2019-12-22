# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
import toml

import logging
logger = logging.getLogger()

config_file = os.getenv('HOME') + '/.pigrizia/hosts.conf'

class UnknownSystem(Exception):
    """
    Raised if the system cannot be detected
    """
    pass

class NotInstalled(Exception):
    """
    Represents something not being installed.
    """
    pass


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
            from pigrizia.command.handler.remote import RemoteHandler
            self.cmdh = RemoteHandler(**kwargs)
        else:
            from pigrizia.command.handler.local import LocalHandler
            self.cmdh = LocalHandler(**kwargs)

def detect_host(**kwargs):
    """
    This will detect the host

    :return: a host object that (hopefully) represents the host at the
        specified address
    :rtype: a subclass of :class:`~pigrizia.host.Host`
    """
    # TODO: this function has to be rewritten, because it is really clumsy.
    # for now it get the job done, however.
    from .linux import (Fedora, Issabel, CentOS, Ubuntu, Proxmox, 
            Debian, Linux)
    
    try:
        config = toml.load(config_file)
    except FileNotFoundError:
        logger.warn("hosts configuration not found")
        config = {}

    # TODO: this could maybe be made a bit simpler?
    if 'addr' not in kwargs and 'name' in kwargs:
        name = kwargs['name']
        if name in config:
            kwargs['config'] = config[name]
            if 'addr' in config[name]:
                kwargs['addr'] = config[name]['addr']

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
