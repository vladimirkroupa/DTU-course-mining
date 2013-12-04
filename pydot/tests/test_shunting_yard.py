import unittest
from pydot.shunting_yard import AndOperator, OrOperator, Course, shunting_yard

class OperatorTest(unittest.TestCase):

    def setUp(self):
        self.and_op = AndOperator()
        self.or_op = OrOperator()

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


class ShuntingYardTest(unittest.TestCase):

    pass