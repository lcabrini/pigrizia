import unittest
from pigrizia.host.linux import Linux

# TODO: this should change name, since the tests are on a local Linux
# system.
class LocalTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_file_exists(self):
        host = Linux()
        self.assertTrue(host.file_exists('/etc/hosts'))
        self.assertFalse(host.file_exists('/etc/non-existent'))

    def test_directory_exists(self):
        host = Linux()
        self.assertTrue(host.directory_exists('/etc'))
        self.assertFalse(host.directory_exists('/non-existent'))

if __name__ == '__main__':
    unittest.main()
