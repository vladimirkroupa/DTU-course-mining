from storage import Storage
from json_decoder import JSONDecoder
import json

class StaticStorage(Storage):
    """Simple implementation using the static courses.json file created by Scrapy.
    """

    def read_course_base(self):
        decoder = JSONDecoder()
        json_file = open('../scraper/courses.json')
        json_data = json.load(json_file)
        return decoder.decode_courses(json_data)

    def last_update_date(self):
        pass

    def store_course_base(self, course_json):
        pass