class CourseRanker:

    def __init__(self, storage):
        self.storage = storage

    def _course_predicate(self, course, department, course_type):
        if department and department != course.department:
            return False
        elif course_type and course_type != course.course_type:
            return False
        else:
            return True

    def course_ranking(self, department = None, course_type = None):
        all_courses = self.storage.list_courses()
        filtered_courses =  [course for course in all_courses if self._course_predicate(course, department, course_type)]
        return filtered_courses
