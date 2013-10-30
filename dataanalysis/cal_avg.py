# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 17:50:17 2013

@author: pascal
"""

#import sys, os
#sys.path.insert(0,'/home/pascal/github/Python-project-Pascal')
##from model.course import Course # NOT NEEDED FOR NOW
#from model.course_run import CourseRun

# current directory must be top-folder (Python-project-Pascal)
# modules MUST use absolute imports (i.e. not relative using dots)
# command: python -m dataanalysis.cal_avg
# in Spyder: use new dedicated interpreter and set its commandline options to "-m dataanalysis.cal_avg"

from model.course_run import CourseRun
from model.course import Course
#from model.department import Department
from storage.static_storage import StaticStorage

def course_run_avg(course_run):
    """ Calculates wga (weighted grade average) for a course run 
    returns wga"""
    grade_sum = 0
    n = 0
    for (grade, count) in course_run.grade_scale.items():
        print grade, count
        grade_sum += int(grade) * count # Important: convert keys/grade to int.
        n += count
    #print "grade_sum is", grade_sum
    #print "n is", n
    try:
        return grade_sum/n # wga
    except ZeroDivisionError:
        return None



def course_avg(course):
<<<<<<< HEAD
    #for course_run in course.course_runs: # OLD, worked 28/10/2013
=======
>>>>>>> b1b4fb215c574dceebaad58f6719a2a033f6798b
    for course_run in course.all_course_runs():
        #print course.code, course.title_en # FOR DEVELOPMENT
        return course_run_avg(course_run)


def department_avg(department=None):
    storage = StaticStorage()
    departments = storage.list_departments() # list all departments
    #departments = storage.list_courses('27')
    avg = {}    
    for department in departments:
        grade_sum = 0
        n = 0
        print department
        for course in department.courses: # NB department.courses is not writting now
            print course.code   
            if course_avg(course) == None:
                #print course_avg(course)
                pass
            else:
                grade_sum += course_avg(course)
                n += 1
        avg[department.code] = grade_sum/n
    return avg    
            
            
        

# 1) func for avg of course run
# 2) func for avg of course
# 3) func for avg of department

#

def main():
    #Course = ...
#    course_run = CourseRun(
#            year = 2006,
#            semester = 'Sommer',
#            students_registered = 0,
#            students_attended = 0,
#            students_passed = 0,
#            not_shown = 0,
#            sick = 0,
#            grade_scale = {'12' : 8,
#               '10' : 27,
#               '7' : 70,
#               '4' : 19,
#               '02' : 12,
#               '00' : 9,
#               '-3' : 4})
#    course_run_avg(course_run)
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

    EXPECTED_COURSES = Course(
            code = '27002',
            language = 'Danish',
            title_en = 'Life Science',
            title_da = 'Biovidenskab',
            evaluation_type = '7 step scale',
            ects_credits = 5,
            course_type = 'BSc',
            course_runs = EXPECTED_COURSE_RUNS)
    
    #course_avg(EXPECTED_COURSES)
    dep_avg = department_avg()
    print dep_avg
    
if __name__ == "__main__":
    main()




#####################################
#
#def numerical_grades(grades):
#    num_grade_scale = [12, 10, 7, 4, 2, 0, -3]
#    # TODO: make unit test
#    # test: length of grades and class?
#    #num_grades = sorted(grades.keys())
#    num_grades = zip(num_grade_scale, sorted(grades.keys()))
#    print num_grades
#    return num_grades
