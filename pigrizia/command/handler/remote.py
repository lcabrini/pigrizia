from getpass import getuser
import paramiko

class RemoteHandler:
    """
    This is a command handler that executes commands on a remote system
    using Paramiko.

    :param str user: the user to use for the SSH connection
    :param str passwd: the password assoctiated with the user
    """

    def __init__(self, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs['user']
        else:
            self.user = getuser()

        if 'passwd' in kwargs:
            self.passwd = kwargs['passwd']
        else:
            # For now we don't do anything, since it is fully possible
            # that the user doesn't need a password (key-based SSH). But
            # we'll keep the else here since I am sure to have forgot
            # something.
            pass

        if 'passphrase' in kwargs:
            # TODO: is this needed? Since I don't know, I will keep it 
            # here for now.
            self.passphrase = kwargs['passphrase']

    def do(self, cmd, **kwargs):
        pass

    def sudo(self, cmd, **kwargs):
        pass

    def interact(self, script, **kwargs):
        pass
