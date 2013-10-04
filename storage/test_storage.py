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

    def testEmptyStorage(self):
        courses = self.test_object.readCourseBase()
        update_date = self.test_object.lastUpdateDate()
        self.assertEqual(None, courses)
        self.assertEqual(None, update_date)

    def testBasicStorageDate(self):
        self.test_object.storeCourseBase(self.EXAMPLE_JSON)
        update_date = self.test_object.lastUpdateDate()
        expected_date = datetime.date.today()
        self.assertEqual(expected_date, update_date, "Date is not today's date.")

    def testBasicStoreRead(self):
        self.test_object.storeCourseBase(self.EXAMPLE_JSON)
        courses = self.test_object.readCourseBase()
        expected_courses = datetime.date.today()
        self.assertEqual(courses, expected_courses, 'Courses read are not the same as courses stored')

if __name__ == '__main__':
    unittest.main()