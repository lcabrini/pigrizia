import unittest
from pigrizia.host.linux import Linux

class LocalTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_foo(self):
        host = Linux()

if __name__ == '__main__':
    unittest.main()
