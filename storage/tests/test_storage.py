import unittest
import datetime

from model.department import Department
from storage.tests.test_dataset import COURSES
from storage.static_storage import StaticStorage

class StorageTest(unittest.TestCase):

    maxDiff = None

    #TODO: path
    test_object = StaticStorage('storage/tests/test_courses.json')

    def test_list_departments(self):
        expected_deps = set([Department('27', 'Department of Systems Biology', None), Department('11', 'Department of Civil Engineering', None)])
        departments = set(self.test_object.list_departments())
        self.assertEqual(expected_deps, departments)

    def test_list_all_courses(self):
        actual_courses = self.test_object.list_all_courses()
        self.assertEqual(COURSES, actual_courses)

    def test_find_department_by_code(self):
        expected = Department('11', 'Department of Civil Engineering', None)
        department= self.test_object.find_department_by_code('11')
        self.assertEqual(expected, department)

    @unittest.skip("TODO")
    def test_empty_storage(self):
        courses = self.test_object.list_all_courses()
        update_date = self.test_object.last_update_date()
        self.assertEqual(None, courses)
        self.assertEqual(None, update_date)

    @unittest.skip("not required ATM")
    def test_basic_storage_date(self):
        self.test_object.store_course_base(self.EXAMPLE_JSON)
        update_date = self.test_object.last_update_date()
        expected_date = datetime.date.today()
        self.assertEqual(expected_date, update_date, "Date is not today's date.")

    @unittest.skip("not required ATM")
    def test_basic_store_read(self):
        self.test_object.store_course_base(self.EXAMPLE_JSON)
        courses = self.test_object.list_all_courses()
        expected_courses = datetime.date.today()
        self.assertEqual(courses, expected_courses, 'Courses read are not the same as courses stored')

if __name__ == '__main__':
    unittest.main()