from storage import Storage
from json_decoder import JSONDecoder
import json

class StaticStorage(Storage):
    """Simple implementation using the static courses.json file created by Scrapy.
    """

    def __init__(self, file_to_use = 'scraper/courses.json'):
        json_file = open(file_to_use)
        self.json_data = json.load(json_file)
        json_file.close()

    def list_departments(self):
        departments = set()
        courses = self.list_courses()
        for course in courses:
            departments.add(course.department)
        return list(departments)

    def find_department_by_code(self, code):
        for department in self.list_departments():
            if department.code == code:
                return department
        return None

    def list_courses(self, department_code = None):
        decoder = JSONDecoder()
        courses = decoder.decode_courses(self.json_data)
        if department_code:
            courses = [course for course in courses if course.department.code == department_code]
        return courses

    def last_update_date(self):
        # TODO: check the creation date of courses.json file
        raise Exception('Not implemented yet.')

    def store_course_base(self, course_json):
        raise Exception('Not implemented.')