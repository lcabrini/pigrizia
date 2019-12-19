# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import unittest
from getpass import getuser, getpass
from pigrizia.command.handler.local import LocalHandler
from pigrizia.command.handler.remote import RemoteHandler
from pigrizia.command.handler import NoSuchCommand

class BaseTestCases:
    class CommandHandlersTestBase(unittest.TestCase):
        user = getuser()

        def test_command(self):
            ret, out, err = self.handler.do("whoami")
            self.assertEqual(ret, 0)
            self.assertEqual(len(out), 1)
            self.assertEqual(out[0], self.user)
            self.assertEqual(len(err), 0)

        def test_invalid_command(self):
            self.assertRaises(NoSuchCommand, self.handler.do, "foo")

class TestLocalCommandHandler(BaseTestCases.CommandHandlersTestBase):
    def setUp(self):
        self.handler = LocalHandler()

class TestRemoteCommandHandler(BaseTestCases.CommandHandlersTestBase):
    passwd = getpass()
    addr = '127.0.0.1'

    def setUp(self):
        self.handler = RemoteHandler(addr=self.addr, user=self.user,
                passwd=self.passwd)

