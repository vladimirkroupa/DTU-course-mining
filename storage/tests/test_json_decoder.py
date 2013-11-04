import unittest
import os
from storage.json_decoder import JSONDecoder
import json
from storage.tests.data import data_dir
from storage.tests.data.test_dataset_evaluations import COURSES

class DecoderTest(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.test_object = JSONDecoder()
        self.json_file = os.path.join(data_dir(), 'test_courses_evaluations.json')

    def test_course_decode(self):
        json_data = open(self.json_file).read()
        courses_dict = json.loads(json_data)
        courses = self.test_object.decode_courses(courses_dict)
        self.assertEquals(COURSES, courses)

if __name__ == '__main__':
    unittest.main()