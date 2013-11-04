from model.course import Course
from model.course_run import CourseRun
from model.department import Department
from model.evaluation import Evaluation
from util.dict_util import tuple_to_dict

def tuple_to_intensity_dict(tuple):
    tuple_to_dict((1, 2, 3, 4, 5), tuple)

COURSE_EVALUATIONS = [
    Evaluation(
        year = 2010,
        semester = u'E',
        could_answer = 174,
        have_answered = 61,
        did_not_follow = 1,
        performance_scale = tuple_to_intensity_dict((4, 11, 37, 8, 1)),
        prereq_scale = tuple_to_intensity_dict((1, 3, 47, 9, 1))
    ),
    Evaluation(
        year = 2011,
        semester = u'F',
        could_answer = 80,
        have_answered = 40,
        did_not_follow = 6,
        performance_scale = tuple_to_intensity_dict((5, 9, 26, 0, 0)),
        prereq_scale = tuple_to_intensity_dict((0, 2, 36, 1, 1))
    )
]

COURSE_RUNS = [
    CourseRun(
        year = 2010,
        semester = u'E',
        students_registered = 169,
        students_attended = 159,
        students_passed = 141,
        not_shown = 9,
        sick = 1,
        grade_scale = {'12' : 12,
                       '10' : 22,
                       '7' : 62,
                       '4' : 26,
                       '02' : 19,
                       '00' : 10,
                       '-3' : 8}
    ),
    CourseRun(
        year = 2011,
        semester = u'F',
        students_registered = 80,
        students_attended = 66,
        students_passed = 61,
        not_shown = 14,
        sick = 0,
        grade_scale = {'12' : 7,
                       '10' : 11,
                       '7' : 23,
                       '4' : 10,
                       '02' : 10,
                       '00' : 2,
                       '-3' : 3}
    )
]


COURSES = [
    Course(
        code = u'27002',
        language = u'Danish',
        title_en = u'Life Science',
        title_da = u'Biovidenskab',
        evaluation_type = u'7 step scale',
        ects_credits = 5,
        course_type = u'BSc',
        course_runs = COURSE_RUNS,
        evaluations = COURSE_EVALUATIONS,
        department = Department(
            code = u'27',
            title_en = u'Department of Systems Biology',
            title_da = None
        )
    )
]