# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 17:50:17 2013

@author: pascal

# 1) func for avg of course run
# 2) func for avg of course
# 3) func for avg of department
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
        #print grade, count
        grade_sum += int(grade) * count # Important: convert keys/grade to int.
        n += count
    try:
        return grade_sum/n # wga
    except ZeroDivisionError:
        return None # kind of NaN, but easier for python to work with



def course_avg(course):
    #for course_run in course.course_runs: # OLD, worked 28/10/2013. List of course_runs
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
        #print department
        for course in department.courses: # NB department.courses is not writting now
            #print course.code   
            if course_avg(course) == None:
                #print course.code, course_avg(course) # FOR DEVELOPMENT, good for finding strange courses.
                # These courses might be new courses without any grade history
                pass
            else:
                grade_sum += course_avg(course)
                n += 1
        #print "grade_sum = {}, n = {}".format(grade_sum,n) # FOR DEVELOPMENT
        avg[department.code] = float(grade_sum)/n # remember to make 
    return avg    
            
            
        


#

def main():
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
