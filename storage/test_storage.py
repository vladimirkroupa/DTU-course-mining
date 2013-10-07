import unittest
import datetime

from storage import Storage

class StorageTest(unittest.TestCase):

    EXAMPLE_JSON = """
        [
            {
                "code": "27002",
                "title_da": "Biovidenskab",
                "language": "Danish",
                "evaluation_type": "7 step scale",
                "title_en": "Life Science",
                "ects_credits": "5",
                "course_type": "BSc",
                "course_runs": [
                    {
                        "semester": "Sommer",
                        "year": "2006"
                    },
                    {
                        "grade_10": "27",
                        "not_shown": "22",
                        "grade_02": "12",
                        "grade_00": "9",
                        "grade_12": "8",
                        "semester": "Vinter",
                        "grade_minus_3": "4",
                        "sick": "1",
                        "year": "2009",
                        "grade_7": "70",
                        "grade_4": "19"
                    }
                ]
            }
        ]"""

    test_object = Storage()

    def test_empty_storage(self):
        courses = self.test_object.read_course_base()
        update_date = self.test_object.last_update_date()
        self.assertEqual(None, courses)
        self.assertEqual(None, update_date)

    def test_basic_storage_date(self):
        self.test_object.store_course_base(self.EXAMPLE_JSON)
        update_date = self.test_object.last_update_date()
        expected_date = datetime.date.today()
        self.assertEqual(expected_date, update_date, "Date is not today's date.")

    def test_basic_store_read(self):
        self.test_object.store_course_base(self.EXAMPLE_JSON)
        courses = self.test_object.read_course_base()
        expected_courses = datetime.date.today()
        self.assertEqual(courses, expected_courses, 'Courses read are not the same as courses stored')

if __name__ == '__main__':
    unittest.main()