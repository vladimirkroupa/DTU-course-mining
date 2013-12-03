import unittest
from model.department import Department
from model.course import Course
from storage.course_repository import CourseRepository

class CourseRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.test_object = CourseRepository()

    def test_store_find_department(self):
        department_1 = Department('24', 'National Veterinary Institute', None)
        department_2 = Department('23', 'National Food Institute', None)
        self.test_object.store_department(department_1)
        self.test_object.store_department(department_2)

        actual_1 = self.test_object.find_department_by_code('24')
        actual_2 = self.test_object.find_department_by_code('23')
        self.assertEqual(department_1, actual_1)
        self.assertEqual(department_2, actual_2)
        self.assertIsNone(self.test_object.find_department_by_code('25'))

    def test_store_find_course(self):
        course = Course(
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

        self.test_object.store_course(course)


if __name__ == '__main__':
    unittest.main()
