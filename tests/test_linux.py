import unittest
from pigrizia.host.linux import Linux

class TestLinux(unittest.TestCase):
    def setUp(self):
        # Not passing an IP address to this makes in local.
        self.host = Linux()

    def tearDown(self):
        pass

    def test_file_exists(self):
        self.assertTrue(self.host.file_exists('/etc/hosts'))
        self.assertFalse(self.host.file_exists('/etc/non-existent'))

    def test_directory_exists(self):
        self.assertTrue(self.host.directory_exists('/etc'))
        self.assertFalse(self.host.directory_exists('/non-existent'))

if __name__ == '__main__':
    unittest.main()
