# -*- coding: utf-8 -*-

import unittest
from scraper.items import CourseItem, DepartmentItem
from model.department import Department
from model.course import Course
from storage.course_repository import CourseRepository

class CourseRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.test_object = CourseRepository()

    def tearDown(self):
        self.test_object.clear()

    def test_store_find_department(self):
        dep_1 = DepartmentItem(code='24', title_en='National Veterinary Institute', title_da=None)
        dep_2 = DepartmentItem(code='23', title_en='National Food Institute', title_da=None)
        self.test_object.store_department_item(dep_1)
        self.test_object.store_department_item(dep_2)

        expected_1 = Department('24', 'National Veterinary Institute', None)
        expected_2 = Department('23', 'National Food Institute', None)
        actual_1 = self.test_object.find_department_by_code('24')
        actual_2 = self.test_object.find_department_by_code('23')
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertIsNone(self.test_object.find_department_by_code('25'))

    def test_store_find_course(self):
        course_1 = CourseItem(
            code = '11120',
            language = 'English',
            title_en = 'Daylight in buildings',
            title_da = u'Dagslys i bygninger',
            evaluation_type = '7 step scale',
            ects_credits = 5.0,
            course_type = 'MSc',
            department = DepartmentItem(
                code = '11',
                title_en = 'Department of Civil Engineering',
                title_da = None
            )
        )

        course_2 = CourseItem(
            code = u'11116',
            language = u'English',
            title_en = u'Sustainable Buildings',
            title_da = u'Energirigtigt byggeri',
            evaluation_type = u'7 step scale',
            ects_credits = 10,
            course_type = u'MSc',
            department = DepartmentItem(
                code = u'11',
                title_en = u'Department of Civil Engineering',
                title_da = None
            )
        )

        expected_1 = Course(
            code = '11120',
            language = 'English',
            title_en = 'Daylight in buildings',
            title_da = u'Dagslys i bygninger',
            evaluation_type = '7 step scale',
            ects_credits = 5.0,
            course_type = 'MSc',
            department = Department(
                code = '11',
                title_en = 'Department of Civil Engineering',
                title_da = None
            )
        )

        expected_2 = Course(
            code = u'11116',
            language = u'English',
            title_en = u'Sustainable Buildings',
            title_da = u'Energirigtigt byggeri',
            evaluation_type = u'7 step scale',
            ects_credits = 10,
            course_type = u'MSc',
            department = Department(
                code = u'11',
                title_en = u'Department of Civil Engineering',
                title_da = None
            )
        )

        dep_1 = DepartmentItem(code='24', title_en='National Veterinary Institute', title_da=None)
        self.test_object.store_department_item(dep_1)

        self.test_object.store_course_item(course_1)
        self.test_object.store_course_item(course_2)
        actual_1 = self.test_object.find_course_by_code('11120')
        actual_2 = self.test_object.find_course_by_code('11116')
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_store_unicode_course(self):
        course = CourseItem(
            code = '11120',
            language = 'English',
            title_en = 'Daylight in buildings',
            title_da = u'Computational Fluid Dynamics vedrørende bygninger',
            evaluation_type = '7 step scale',
            ects_credits = 5.0,
            course_type = 'MSc',
            department = DepartmentItem(
                code = '11',
                title_en = 'Department of Civil Engineering',
                title_da = None
            )
        )

        self.test_object.store_course_item(course)

        expected = Course(
            code = '11120',
            language = 'English',
            title_en = 'Daylight in buildings',
            title_da = u'Computational Fluid Dynamics vedrørende bygninger',
            evaluation_type = '7 step scale',
            ects_credits = 5.0,
            course_type = 'MSc',
            department = Department(
                code = '11',
                title_en = 'Department of Civil Engineering',
                title_da = None
            )
        )

        actual = self.test_object.find_course_by_code('11120')
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
