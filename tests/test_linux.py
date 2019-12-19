# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import unittest
from getpass import getuser, getpass
from pigrizia.host.linux import Linux

class BaseTestCases:
    class LinuxTestBase(unittest.TestCase):
        def test_file_exists(self):
            self.assertTrue(self.host.file_exists('/etc/hosts'))
            self.assertFalse(self.host.file_exists('/etc/foo'))

        def test_directory_exists(self):
            self.assertTrue(self.host.directory_exists('/etc'))
            self.assertFalse(self.host.directory_exists('/foo'))

class TestLocalLinux(BaseTestCases.LinuxTestBase):
    def setUp(self):
        self.host = Linux()

class TestRemoteLinux(BaseTestCases.LinuxTestBase):
    user = getuser()
    passwd = getpass()
    addr = '127.0.0.1'

    def setUp(self):
        self.host = Linux(addr=self.addr, user=self.user, 
                passwd=self.passwd)

if __name__ == '__main__':
    unittest.main()
