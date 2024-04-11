import unittest

from main import *


class MyTestCase(unittest.TestCase):
    def test_get_information(self):
        print('nihao')
        get_information('你')


if __name__ == '__main__':
    unittest.main()
