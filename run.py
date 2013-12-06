import argparse
import sys
from storage.course_repository import CourseRepository

repo = CourseRepository('sqlite:///courses.db')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course_code", help="course code")
    parser.add_argument("-t", "--transitive", help="prints transitive graph", action="store_true")
    args = parser.parse_args()
    code = args.course_code
    transitive = args.transitive

    if not transitive:
        plot_course_graph(code)
    else:
        plot_course_trans_graph(code)

def plot_course_graph(code):
    course = repo.find_course_by_code(code)
    if not course:
        sys.exit("Course " + code + " not found in database.")
    graph = course.prereq_graph()
    graph.write(code+'.png', format='png')

def plot_course_trans_graph(code):
    course = repo.find_course_by_code(code)
    if not course:
        sys.exit("Course " + code + " not found in database.")
    graph = course.transitive_prereq_graph(repo, 0)
    graph.write(code+'_trans.png', format='png')

if  __name__ =='__main__':
    main()