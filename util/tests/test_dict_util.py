import unittest
from util.dict_util import tuple_to_dict

class DictUtilTest(unittest.TestCase):

    def test_tuple_to_dict(self):
        tuple = (0, 1, 5, 3, 1)
        keys = [1, 2, 3, 4, 5]
        expected = {1: 0, 2: 1, 3: 5, 4: 3, 5: 1}
        actual = tuple_to_dict(keys, tuple)
        self.assertEqual(expected, actual)