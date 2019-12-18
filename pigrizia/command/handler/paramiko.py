import paramiko

class ParamikoHandler:
    """
    This is a command handler that executes commands on a remote system
    using Paramiko.

    :param str user: the user to use for the SSH connection
    :param str passwd: the password assoctiated with the user
    """

    def __init__(self, user, passwd, **kwargs):
        self.user = user
        self.passwd = passwd

    def do(self, cmd, **kwargs):
        pass

    def sudo(self, cmd, **kwargs):
        pass

    def interact(self, script, **kwargs):
        pass
