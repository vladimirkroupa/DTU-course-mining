from storage.static_storage import StaticStorage
from ranker.course_ranker import CourseRanker

STORAGE = StaticStorage()


def list_departments():
    return STORAGE.list_departments()

def course_ranking(self, department_code = None, course_type = None):
    department = STORAGE.find_department_by_code(department_code)
    course_ranker = CourseRanker(STORAGE)
    return course_ranker.course_ranking(department, course_type)

if __name__ == '__main__':
    print(course_ranking('27002', 'MSc'))