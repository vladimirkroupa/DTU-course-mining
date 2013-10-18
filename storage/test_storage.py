import unittest
import datetime

from model.department import Department
from static_storage import StaticStorage

class StorageTest(unittest.TestCase):

    #TODO: rely on presence of the file?
    test_object = StaticStorage('scraper/courses.json')

    def test_list_departments(self):
        expected_deps = [Department('27', 'Department of Systems Biology', None), Department('11', 'Department of Civil Engineering')]
        departments = self.test_object.list_departments()
        self.assertEqual(expected_deps, departments)

    @unittest.skip("TODO")
    def test_empty_storage(self):
        courses = self.test_object.read_course_base()
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
        courses = self.test_object.read_course_base()
        expected_courses = datetime.date.today()
        self.assertEqual(courses, expected_courses, 'Courses read are not the same as courses stored')

if __name__ == '__main__':
    unittest.main()