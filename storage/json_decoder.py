from model.course_run import CourseRun
import json

class JSONDecoder():

    def decode_courses(self, course_json):
        print course_json
        pass

    def decode_course_runs(self, course_run_json):
        return [self.decode_course_run(dict) for dict in json.loads(course_run_json)]

    def decode_course_run(self, cr):
        grades = {}
        grades['12'] = int(cr.get('grade_12'))
        grades['10'] = int(cr.get('grade_10'))
        grades['7'] = int(cr.get('grade_7'))
        grades['4'] = int(cr.get('grade_4'))
        grades['02'] = int(cr.get('grade_02'))
        grades['00'] = int(cr.get('grade_00'))
        grades['-3'] = int(cr.get('grade_minus_3'))

        if not grades:
            grades = None

        return CourseRun(
            year = int(cr.get('year')),
            semester = cr.get('semester'),
            students_registered = int(cr.get('students_registered')),
            students_attended = int(cr.get('students_attended')),
            students_passed = int(cr.get('students_passed')),
            not_shown = int(cr.get('not_shown')),
            sick = int(cr.get('sick')),
            grade_scale = grades
        )