from storage import Storage
from json_decoder import JSONDecoder
import json

class StaticStorage(Storage):
    """Simple implementation using the static courses.json file created by Scrapy.
    """

    def __init__(self, file_to_use = '../scraper/courses.json'):
        self.file = file_to_use

    def read_course_base(self):
        decoder = JSONDecoder()
        json_file = open(self.file)
        json_data = json.load(json_file)
        return decoder.decode_courses(json_data)

    def last_update_date(self):
        # TODO: check the creation date of courses.json file
        raise Exception('Not implemented yet.')

    def store_course_base(self, course_json):
        raise Exception('Not implemented.')