import matplotlib.pyplot as plt
import numpy as np
from dataanalysis.cal_avg import department_avg, course_avg, course_run_avg
#from dataanalysis.cal_avg import course_avg





#plt.figure(1)
#plt.plot([1, 4, 4, 2, 2, -1, -2, -4, 8, 7])
#plt.xlabel("Time")
#plt.ylabel("Amplitude")
#plt.title("Curve")
##plt.savefig("curve.png") # Could also have written svg, png, ...
#plt.show()

# 21 departments



def list_all_courses(department, year):
    courses = []
    for course in department.courses:
        if course_has_year():
            courses.append(course)
    return courses

def course_has_year(course, year):
    for course_run in course.all_course_runs():
        if course_run.year == year:
            return True
    return False


# Aim: calculate department average for each year

#3)

def list_avg(mylist):
    try:
        return sum(mylist)/len(mylist)
    except ZeroDivisionError:
        return None


def department_year_avg(department, year):
    """ Calculates department average for one year """
    course_avgs = []
    for course in list_all_courses(department, year):
        course_runs = course.get_course_run_year(year) #Vladimir comes!!!! returns list!
        course_run_avgs = []            
        for course_run in course_runs:
            course_run_avgs.append(course_run_avg(course_run))
        course_avg = list_avg(course_run_avgs) 
        course_avgs.append(course_avg)
    return list_avg(course_avgs) # returns average

def department_all_years_avgs(department):
    year_avgs = []
    for year in department.list_all_years(): # Vladimir comes
        year_avg = department_year_avg(department, year)
        year_avgs.append(year_avg)
    return year_avgs


def deparment_:
    for department in list_all_departments():

#2008:2013
