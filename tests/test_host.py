# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import unittest
from getpass import getuser, getpass
from pigrizia.host import get_host

class BaseTestCases:
    class HostTestBase(unittest.TestCase):
        user = getuser()
        passwd = getpass()

class TestLocalHost(BaseTestCases.HostTestBase):
    def test_get_host(self):
        # Works for me, change as needed for your tests.
        os = 'fedora'
        host = get_host(passwd=self.passwd)
        self.assertEqual(host.distro(), os)

class TestRemoteHost(BaseTestCases.HostTestBase):
    addr = '127.0.0.1'

    def test_get_host(self):
        # Change if you need to.
        os = 'fedora'
        host = get_host(addr=self.addr, user=self.user, 
                passwd=self.passwd)
        self.assertEqual(host.distro(), os)
