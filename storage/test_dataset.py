from model.course import Course
from model.course_run import CourseRun
from model.department import Department

COURSE_RUNS_SB = [
    CourseRun(
        year = 2007,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 2,
        sick = 0,
        grade_scale = {'12' : 4,
                       '10' : 10,
                       '7' : 15,
                       '4' : 2,
                       '02' : 0,
                       '00' : 1,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2008,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 1,
        sick = 0,
        grade_scale = {'12' : 10,
                       '10' : 14,
                       '7' : 6,
                       '4' : 0,
                       '02' : 0,
                       '00' : 0,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2009,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 1,
        sick = 0,
        grade_scale = {'12' : 5,
                       '10' : 25,
                       '7' : 11,
                       '4' : 0,
                       '02' : 0,
                       '00' : 1,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2010,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 2,
        sick = 0,
        grade_scale = {'12' : 6,
                       '10' : 28,
                       '7' : 35,
                       '4' : 2,
                       '02' : 0,
                       '00' : 1,
                       '-3' : 1}
    ),
    CourseRun(
        year = 2011,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 0,
        sick = 0,
        grade_scale = {'12' : 27,
                       '10' : 24,
                       '7' : 6,
                       '4' : 0,
                       '02' : 0,
                       '00' : 0,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2012,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 13,
        sick = 0,
        grade_scale = {'12' : 10,
                       '10' : 23,
                       '7' : 23,
                       '4' : 2,
                       '02' : 5,
                       '00' : 0,
                       '-3' : 0}
    )]

COURSE_RUNS_DIB = [
    CourseRun(
        year = 2007,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 2,
        sick = 0,
        grade_scale = {'12' : 5,
                       '10' : 6,
                       '7' : 11,
                       '4' : 0,
                       '02' : 1,
                       '00' : 1,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2008,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 1,
        sick = 0,
        grade_scale = {'12' : 3,
                       '10' : 19,
                       '7' : 2,
                       '4' : 1,
                       '02' : 1,
                       '00' : 0,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2009,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 2,
        sick = 0,
        grade_scale = {'12' : 4,
                       '10' : 19,
                       '7' : 12,
                       '4' : 0,
                       '02' : 0,
                       '00' : 0,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2011,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 8,
        sick = 0,
        grade_scale = {'12' : 11,
                       '10' : 17,
                       '7' : 8,
                       '4' : 3,
                       '02' : 0,
                       '00' : 0,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2012,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 6,
        sick = 0,
        grade_scale = {'12' : 9,
                       '10' : 14,
                       '7' : 19,
                       '4' : 7,
                       '02' : 0,
                       '00' : 1,
                       '-3' : 0}
    ),
    CourseRun(
        year = 2010,
        semester = 'E',
        students_registered = 0,
        students_attended = 0,
        students_passed = 0,
        not_shown = 0,
        sick = 0,
        grade_scale = {'12' : 23,
                       '10' : 16,
                       '7' : 14,
                       '4' : 3,
                       '02' : 0,
                       '00' : 0,
                       '-3' : 1}
    )]

COURSE_RUNS_AIB = [
    CourseRun(
    year = 2012,
    semester = 'E',
    students_registered = 0,
    students_attended = 0,
    students_passed = 0,
    not_shown = 2,
    sick = 0,
    grade_scale = {'12' : 6,
                   '10' : 13,
                   '7' : 0,
                   '4' : 1,
                   '02' : 0,
                   '00' : 0,
                   '-3' : 0}
    )]


COURSES = [
    Course(
        code = '11116',
        language = 'English',
        title_en = 'Sustainable Buildings',
        title_da = 'Energirigtigt byggeri',
        evaluation_type = '7 step scale',
        ects_credits = 10,
        course_type = 'MSc',
        course_runs = COURSE_RUNS_SB,
        department = Department(
            code = '11',
            title_en = 'Department of Civil Engineering',
            title_da = None
        )
    ),
    Course(
        code = '11120',
        language = 'English',
        title_en = 'Daylight in buildings',
        title_da = 'Dagslys i bygninger',
        evaluation_type = '7 step scale',
        ects_credits = 5,
        course_type = 'MSc',
        course_runs = COURSE_RUNS_DIB,
        department = Department(
            code = '11',
            title_en = 'Department of Civil Engineering',
            title_da = None
        )
    ),
    Course(
        code = '27625',
        language = 'English',
        title_en = 'Algorithms in bioinformatics',
        title_da = 'Algoritmer i bioinformatik',
        evaluation_type = '7 step scale',
        ects_credits = 5,
        course_type = 'MSc',
        course_runs = COURSE_RUNS_AIB,
        department = Department(
            code = '27',
            title_en = 'Department of Systems Biology',
            title_da = None
        )
    )
]