from model.course_run import CourseRun
from model.course import Course
from model.department import Department
from model.evaluation import Evaluation
import json

class JSONDecoder():

    def decode_courses(self, course_json):
        return [self.decode_course(dict) for dict in course_json]

    def decode_course(self, course_dict):
        cr_json = course_dict.get('course_runs')
        course_runs = self.decode_course_runs(cr_json)
        dep_json = course_dict.get('department')
        department = self.decode_department(dep_json)
        evaluation_json = course_dict.get('evaluations')
        evaluations =  self.decode_evaluations(evaluation_json)

        course = Course(
            code = course_dict['code'],
            language = course_dict['language'],
            title_en = course_dict['title_en'],
            title_da = course_dict['title_da'],
            evaluation_type = course_dict['evaluation_type'],
            ects_credits = float(course_dict['ects_credits'].replace(",", ".")),
            course_type = course_dict['course_type'],
            department = department
        )
        for run in course_runs:
            course.add_course_run(run)

        for evaluation in evaluations:
            course.add_evaluation(evaluation)

        return course

    def decode_course_runs(self, course_run_dicts):
        return [self.decode_course_run(dict) for dict in course_run_dicts]

    def decode_course_run(self, cr):
        grades = {}
        grades['12'] = int(cr.get('grade_12', 0))
        grades['10'] = int(cr.get('grade_10', 0))
        grades['7'] = int(cr.get('grade_7', 0))
        grades['4'] = int(cr.get('grade_4', 0))
        grades['02'] = int(cr.get('grade_02', 0))
        grades['00'] = int(cr.get('grade_00', 0))
        grades['-3'] = int(cr.get('grade_minus_3', 0))

        return CourseRun(
            year = int(cr.get('year')),
            semester = self.parse_semester(cr['semester']),
            students_registered = int(cr.get('students_registered', 0)),
            students_attended = int(cr.get('students_attended', 0)),
            students_passed = int(cr.get('students_passed', 0)),
            not_shown = int(cr.get('not_shown', 0)),
            sick = int(cr.get('sick', 0)),
            grade_scale = grades
        )

    def parse_semester(self, semester):
        if semester == 'Winter':
            return 'E'
        elif semester == 'Summer':
            return 'F'
        elif semester == 'January':
            return 'Jan'
        raise Exception("Unknown semester value: " + semester)

    def decode_department(self, department_json):
        return Department(
            code = department_json['code'],
            title_en = department_json['title_en'],
            title_da = department_json.get('title_da')
    )

    def decode_evaluations(self, evaluations_dicts):
        return [self.decode_evaluation(dict) for dict in evaluations_dicts]

    def decode_evaluation(self, evaluation_dict):

        performance_scale = {}
        performance_scale[1] = int(evaluation_dict.get('performance_much_less', 0))
        performance_scale[2] = int(evaluation_dict.get('performance_less', 0))
        performance_scale[3] = int(evaluation_dict.get('performance_same', 0))
        performance_scale[4] = int(evaluation_dict.get('performance_more', 0))
        performance_scale[5] = int(evaluation_dict.get('performance_much_more', 0))

        prereq_scale = {}
        prereq_scale[1] = int(evaluation_dict.get('prereq_too_low', 0))
        prereq_scale[2] = int(evaluation_dict.get('prereq_low', 0))
        prereq_scale[3] = int(evaluation_dict.get('prereq_adequate', 0))
        prereq_scale[4] = int(evaluation_dict.get('prereq_high', 0))
        prereq_scale[5] = int(evaluation_dict.get('prereq_too_high', 0))

        return Evaluation(
            year = int(evaluation_dict['year']),
            semester = self.parse_semester(evaluation_dict['semester']),
            could_answer = int(evaluation_dict['could_answer']),
            have_answered = int(evaluation_dict['have_answered']),
            did_not_follow = int(evaluation_dict['did_not_follow']),
            performance_scale = performance_scale,
            prereq_scale = prereq_scale
        )