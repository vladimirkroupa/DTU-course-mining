import unittest
from viz.shunting_yard import AllOf, AnyOf

class OperatorTest(unittest.TestCase):

    def setUp(self):
        self.and_op = AllOf()
        self.or_op = AnyOf()

    def test_lt(self):
        self.assertLess(self.and_op, self.or_op)

    def test_gt(self):
        self.assertGreater(self.or_op, self.and_op)

    def test_eq(self):
        self.assertEqual(self.or_op, self.or_op)
        self.assertEqual(self.and_op, self.and_op)

    def test_ne(self):
        self.assertNotEqual(self.and_op, self.or_op)
        self.assertNotEqual(self.or_op, self.and_op)
