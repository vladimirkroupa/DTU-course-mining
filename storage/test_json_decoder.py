import unittest
from model.course import Course
from model.course_run import CourseRun
from json_decoder import JSONDecoder
import json

class DecoderTest(unittest.TestCase):

    COURSE_RUNS_JSON = """
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
        },
        {
            "semester": "Sommer",
            "year": "2006"
        }
    ]"""

    COURSES_JSON =  """
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

    EXPECTED_COURSE_RUNS = [
        CourseRun(
            year = 2009,
            semester = 'Vinter',
            students_registered = 0,
            students_attended = 0,
            students_passed = 0,
            not_shown = 22,
            sick = 1,
            grade_scale = {'12' : 8,
                           '10' : 27,
                           '7' : 70,
                           '4' : 19,
                           '02' : 12,
                           '00' : 9,
                           '-3' : 4}
        ),
        CourseRun(
            year = 2006,
            semester = 'Sommer',
            students_registered = 0,
            students_attended = 0,
            students_passed = 0,
            not_shown = 0,
            sick = 0,
            grade_scale = {}
        )]

    EXPECTED_COURSES = [
        Course(
            code = '27002',
            language = 'Danish',
            title_en = 'Life Science',
            title_da = 'Biovidenskab',
            evaluation_type = '7 step scale',
            ects_credits = 5,
            course_type = 'BSc',
            course_runs = EXPECTED_COURSE_RUNS
        )
    ]

    test_object = JSONDecoder()


    def test_basic_course_decode(self):
        courses = self.test_object.decode_courses(self.COURSES_JSON)
        self.assertEquals(self.EXPECTED_COURSES, courses)

    def test_basic_course_run_decode(self):
        course_runs_dict = json.loads(self.COURSE_RUNS_JSON)
        course_runs = self.test_object.decode_course_runs(course_runs_dict)
        self.assertEquals(self.EXPECTED_COURSE_RUNS, course_runs)

if __name__ == '__main__':
    unittest.main()