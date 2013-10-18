from storage import Storage
from json_decoder import JSONDecoder
import json

class StaticStorage(Storage):
    """Simple implementation using the static courses.json file created by Scrapy.
    """

    def __init__(self, file_to_use = '../scraper/courses.json'):
        self.file = file_to_use
        json_file = open(self.file)
        self.json_data = json_file.read()
        json_file.close()

    def list_departments(self):
        departments = set()
        courses = self.read_course_base()
        for course in courses:
            departments.add(course.department)
        return list(departments)

    def read_course_base(self):
        decoder = JSONDecoder()
        return decoder.decode_courses(self.json_data)

    def last_update_date(self):
        # TODO: check the creation date of courses.json file
        raise Exception('Not implemented yet.')

    def store_course_base(self, course_json):
        raise Exception('Not implemented.')