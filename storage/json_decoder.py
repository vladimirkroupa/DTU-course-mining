from model.course_run import CourseRun
import json

class JSONDecoder():

    def decode_courses(self, course_json):
        pass

    def decode_course_runs(self, course_run_json):
        return [self.decode_course_run(dict) for dict in json.loads(course_run_json)]

    def decode_course_run(self, cr):
        grades = {}
        grades['12'] = int(cr.get('grade_12', 0))
        grades['10'] = int(cr.get('grade_10', 0))
        grades['7'] = int(cr.get('grade_7', 0))
        grades['4'] = int(cr.get('grade_4', 0))
        grades['02'] = int(cr.get('grade_02', 0))
        grades['00'] = int(cr.get('grade_00', 0))
        grades['-3'] = int(cr.get('grade_minus_3', 0))

        if not grades:
            grades = None

        return CourseRun(
            year = int(cr.get('year')),
            semester = cr.get('semester'),
            students_registered = int(cr.get('students_registered', 0)),
            students_attended = int(cr.get('students_attended', 0)),
            students_passed = int(cr.get('students_passed', 0)),
            not_shown = int(cr.get('not_shown', 0)),
            sick = int(cr.get('sick', 0)),
            grade_scale = grades
        )