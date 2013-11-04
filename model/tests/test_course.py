import unittest

from storage.tests.data.test_dataset_evaluations import COURSES

class CourseTest(unittest.TestCase):

    def setUp(self):
        self.course = COURSES[0]

    def test_list_years_run(self):
        expected = set([2010, 2011])
        actual = self.course.list_years_run()
        self.assertEquals(expected, actual)