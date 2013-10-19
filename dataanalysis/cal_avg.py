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


def course_run_avg(course_run):
    grade_sum = 0
    n = 0
    for (grade, count) in course_run.grade_scale.items():
        #print grade, count
        grade_sum += int(grade) * count
        n += count
    wga = grade_sum/n
    print wga
# rembemer to convert keys to int.



# 1) func for avg of course run
# 2) func for avg of course
# 3) func for avg of department

#

def main():
    #Course = ...
    course_run = CourseRun(
            year = 2006,
            semester = 'Sommer',
            students_registered = 0,
            students_attended = 0,
            students_passed = 0,
            not_shown = 0,
            sick = 0,
            grade_scale = {'12' : 8,
               '10' : 27,
               '7' : 70,
               '4' : 19,
               '02' : 12,
               '00' : 9,
               '-3' : 4})
    course_run_avg(course_run)

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
