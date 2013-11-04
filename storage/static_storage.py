from storage import Storage
from json_decoder import JSONDecoder
import json
import os
from storage import __file__ as json_data_dir

def storage_data_file():
    return os.path.join(os.path.dirname(json_data_dir), '..', 'data', 'courses.json')

class StaticStorage(Storage):
    """Simple implementation using the static courses.json file created by Scrapy.
    """

    def __init__(self, file_to_use = storage_data_file()):
        self.departments = {}
        json_file = open(file_to_use)
        json_data = json.load(json_file)
        json_file.close()
        self._load_departments(json_data)

    def _load_departments(self, json_data):
        decoder = JSONDecoder()
        courses = decoder.decode_courses(json_data)

        for course in courses:
            dep_code = course.department.code
            if not self.departments.has_key(dep_code):
                self.departments[dep_code] = course.department

            department = self.departments[dep_code]
            department.add_course(course)

    def list_departments(self):
        return self.departments.values()

    def find_department_by_code(self, code):
        return self.departments.get(code)

    def list_all_courses(self):
        all_courses = []
        for department in self.departments.values():
            all_courses.extend(department.courses)
        return all_courses

    def last_update_date(self):
        # TODO: check the creation date of courses.json file
        raise Exception('Not implemented yet.')

    def store_course_base(self, course_json):
        raise Exception('Not implemented.')