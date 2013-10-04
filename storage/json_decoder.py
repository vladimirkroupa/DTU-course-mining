from model.course_run import CourseRun
import json

class JSONDecoder():

    def decodeCourses(self, course_json):
        pass

    def decodeCourseRuns(self, course_run_json):
        cr_dicts = json.loads(course_run_json)
        for dict in cr_dicts:
            return self.decodeCourseRun(dict)

    def decodeCourseRun(self, cr):
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
            year = cr.get('year'),
            semester = cr.get('semester'),
            students_registered = cr.get('students_registered'),
            students_attended = cr.get('students_attended'),
            students_passed = cr.get('students_passed'),
            not_shown = cr.get('not_shown'),
            sick = cr.get('sick'),
            grade_scale = grades
        )