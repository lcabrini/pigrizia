# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import unittest
import os
import tempfile
from getpass import getuser, getpass
from pigrizia.host.linux import Linux
from pigrizia.service.user import UserExists, NoSuchUser

checksum = "730c3c44ec7fd5d7392a5e41a472b3c495be4179527ee45ce899b239e9df1fdd1ee08e5b62dc460f73a4f39ce8be8120adb4e7bacc6864f09ce35bdffa90e816"

class BaseTestCases:
    class LinuxTestBase(unittest.TestCase):
        user = getuser()
        passwd = getpass()

        def test_file_exists(self):
            self.assertTrue(self.host.file_exists('/etc/hosts'))
            self.assertFalse(self.host.file_exists('/etc/foo'))

        def test_directory_exists(self):
            self.assertTrue(self.host.directory_exists('/etc'))
            self.assertFalse(self.host.directory_exists('/foo'))

        def test_mkdir_and_rmdir(self):
            self.assertFalse(self.host.directory_exists('/tmp/foo'))
            self.assertEqual(self.host.mkdir('/tmp/foo'), 0)
            self.assertTrue(self.host.directory_exists('/tmp/foo'))
            self.assertEqual(self.host.rmdir('/tmp/foo'), 0)
            self.assertFalse(self.host.directory_exists('/tmp/foo'))

        def test_whoami(self):
            self.assertEqual(self.host.whoami(), self.user)
            self.assertEqual(self.host.whoami(sudo=True), 'root')

        def test_user_exists(self):
            self.assertTrue(self.host.user_exists('root'))
            self.assertFalse(self.host.user_exists('foobar'))

        def test_user_add_and_delete(self):
            user="foobar"
            passwd="barfoo"
            self.assertFalse(self.host.user_exists(user))
            self.assertTrue(self.host.useradd(user=user, passwd=passwd))
            self.assertTrue(self.host.user_exists(user))
            self.assertTrue(self.host.userdel(user=user))
            self.assertFalse(self.host.user_exists(user))

        def test_adding_existing_user(self):
            self.assertRaises(UserExists, self.host.useradd, "root")

        def test_removing_nonexisting_user(self):
            self.assertRaises(NoSuchUser, self.host.userdel, "bimbaz")

        def test_set_permissions(self):
            fp, fname = tempfile.mkstemp()
            self.host.set_permissions(fname, permission=0o666)
            stat = os.stat(fname)
            perm = oct(stat.st_mode) and 0o666
            fp.close()
            self.assertEqual(perm, 0o666)

        def test_mktemp(self):
            tmpfile = self.host.mktemp()
            # TODO: maybe this is dumb, since $TMPDIR might be set to
            # a different location.
            self.assertTrue(tmpfile.startswith("/tmp/"))
            # TODO: we should probably remove tmpfile after we are done.

        def test_read_write_file(self):
            f = "foo.txt"
            t = "Foo\nBar\nBim\nBaz\n"
            self.host.write_file(f, t)
            t2 = self.host.read_file(f)
            self.assertEqual(t, t2)
            # TODO: add this when we have rm command
            # self.host.rm(f)

        def test_checksum(self):
            f = "foo.txt"
            t = "Foo\nBar\nBim\nBaz\n"
            self.host.write_file(f, t)
            cs = self.host.checksum(f)
            self.assertEqual(cs, checksum)
            

class TestLocalLinux(BaseTestCases.LinuxTestBase):
    def setUp(self):
        self.host = Linux(user=self.user, passwd=self.passwd)

class TestRemoteLinux(BaseTestCases.LinuxTestBase):
    addr = '127.0.0.1'

    def setUp(self):
        self.host = Linux(addr=self.addr, user=self.user, 
                passwd=self.passwd)

if __name__ == '__main__':
    unittest.main()
