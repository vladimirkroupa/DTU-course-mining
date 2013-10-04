import unittest
from model.course import Course
from model.course_run import CourseRun
from json_decoder import JSONDecoder
import json

class StorageTest(unittest.TestCase):

    EXAMPLE_COURSE_RUN = """
    [
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
    ]"""

    EXAMPLE_COURSE =  """
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

    test_object = JSONDecoder()

    def testBasisCourseDecodes(self):
        self.fail('Test not implemented.')

    def testBasisCourseRunDecodes(self):
        expected_course_runs = [CourseRun(
            year = 2009,
            semester = 'Vinter',
            students_registered = None,
            students_attended = None,
            students_passed = None,
            not_shown = 22,
            sick = 1,
            grade_scale = {'12' : 8,
                           '10' : 27,
                           '7' : 70,
                           '4' : 19,
                           '02' : 12,
                           '00' : 9,
                           '-3' : 4}
        )]
        course_runs = self.test_object.decodeCourseRuns(self.EXAMPLE_COURSE_RUN)
        self.assertEqual(expected_course_runs, course_runs)

if __name__ == '__main__':
    unittest.main()