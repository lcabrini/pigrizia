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

    def __init__(self, **kwargs):
        if 'addr' in kwargs and not kwargs['addr'] is None:
            from pigrizia.command.handler.remote import RemoteHandler
            self.cmdh = RemoteHandler(**kwargs)
        else:
            from pigrizia.command.handler.local import LocalHandler
            self.cmdh = LocalHandler(**kwargs)

