import unittest
import os
from scraper.spiders.coursespider import CourseRunParser
from util.scrapy_testutils import fake_response_from_file
from scraper.spiders.tests import __file__ as test_directory
from scraper.items import CourseItem
from scraper.spiders.page_counter import PageCounter
from scraper.spiders.coursespider import CourseSpider
from scraper.spiders.tests.data import data_dir

class CourseRunParserTest(unittest.TestCase):

    def setUp(self):
        self.course_run_parser = CourseRunParser(log = CourseSpider().log)
        self.course_27002_course_run_page = os.path.join(data_dir(), '27002_course_run_summer_2010.html')
        self.course_run_two_scales = os.path.join(data_dir(), 'Course_run_two_scales.html')
        self.not_enough_grades = os.path.join(data_dir(), 'Course_run_not_enough_grades.html')
        self.missing_passed = os.path.join(data_dir(), 'Course_run_missing_passed.html')
        self.mixed_scales = os.path.join(data_dir(), 'Course_run_mixed_scales.html')

    def test_parse_grade_dist_page(self):
        response = fake_response_from_file(self.course_27002_course_run_page)
        response.meta['course'] = CourseItem(course_runs = [], code = '27002')
        response.meta['counter'] = PageCounter(1, 0)
        course_item = self.course_run_parser.parse_grade_dist_page(response)
        course_run = course_item['course_runs'][0]

        self.assertEqual(u'2010', course_run['year'])
        self.assertEqual(u'Summer', course_run['semester'])
        self.assertEqual(u'74', course_run['students_registered'])
        self.assertEqual(u'61', course_run['students_attended'])
        self.assertEqual(u'45', course_run['students_passed'])
        #self.assertEqual(u'4.7', course_run['exam_average'])
        self.assertEqual(u'2', course_run['grade_12'])
        self.assertEqual(u'10', course_run['grade_10'])
        self.assertEqual(u'21', course_run['grade_7'])
        self.assertEqual(u'7', course_run['grade_4'])
        self.assertEqual(u'5', course_run['grade_02'])
        self.assertEqual(u'8', course_run['grade_00'])
        self.assertEqual(u'8', course_run['grade_minus_3'])
        self.assertEqual(u'2', course_run['sick'])
        self.assertEqual(u'11', course_run['not_shown'])

    def test_parse_grade_dist_two_grade_scales(self):
        response = fake_response_from_file(self.course_run_two_scales)
        response.meta['course'] = CourseItem(course_runs = [], code = '11B12')
        response.meta['counter'] = PageCounter(1, 0)

        course_item = self.course_run_parser.parse_grade_dist_page(response)
        course_run = course_item['course_runs'][0]

        self.assertEqual(u'2004', course_run['year'])
        self.assertEqual(u'Winter', course_run['semester'])
        self.assertEqual(u'24', course_run['students_registered'])
        self.assertEqual(u'18', course_run['students_attended'])
        self.assertEqual(u'18', course_run['students_passed'])
        self.assertEqual(u'0', course_run['grade_12'])
        self.assertEqual(u'11', course_run['grade_10'])
        self.assertEqual(u'7', course_run['grade_7'])
        self.assertEqual(u'0', course_run['grade_4'])
        self.assertEqual(u'0', course_run['grade_02'])
        self.assertEqual(u'0', course_run['grade_00'])
        self.assertEqual(u'0', course_run['grade_minus_3'])
        self.assertEqual(u'6', course_run['not_shown'])

    def test_parse_grade_dist_not_enough_grades(self):
        response = fake_response_from_file(self.not_enough_grades)
        response.meta['course'] = CourseItem(course_runs = [], code = '11130')
        response.meta['counter'] = PageCounter(1, 0)

        course_item = self.course_run_parser.parse_grade_dist_page(response)
        course_run = course_item['course_runs'][0]

        self.assertEqual(u'2012', course_run['year'])
        self.assertEqual(u'Winter', course_run['semester'])
        self.assertEqual(u'2', course_run['students_registered'])
        self.assertEqual(u'1', course_run['students_attended'])

    def test_parse_grade_dist_missing_passed(self):
        response = fake_response_from_file(self.missing_passed)
        response.meta['course'] = CourseItem(course_runs = [], code = '11126')
        response.meta['counter'] = PageCounter(1, 0)

        course_item = self.course_run_parser.parse_grade_dist_page(response)
        course_run = course_item['course_runs'][0]

        self.assertEqual(u'2011', course_run['year'])
        self.assertEqual(u'Winter', course_run['semester'])
        self.assertEqual(u'2', course_run['students_registered'])
        self.assertEqual(u'2', course_run['students_attended'])
        self.assertEqual(u'1', course_run['grade_12'])
        self.assertEqual(u'0', course_run['grade_10'])
        self.assertEqual(u'0', course_run['grade_7'])
        self.assertEqual(u'0', course_run['grade_4'])
        self.assertEqual(u'0', course_run['grade_02'])
        self.assertEqual(u'0', course_run['grade_00'])
        self.assertEqual(u'1', course_run['grade_minus_3'])

    def test_parse_grade_dist_mixed_scales(self):
        response = fake_response_from_file(self.mixed_scales)
        response.meta['course'] = CourseItem(course_runs = [], code = '27944')
        response.meta['counter'] = PageCounter(1, 0)

        course_item = self.course_run_parser.parse_grade_dist_page(response)
        course_run = course_item['course_runs'][0]

        self.assertEqual(u'2012', course_run['year'])
        self.assertEqual(u'Summer', course_run['semester'])
        self.assertEqual(u'23', course_run['students_registered'])
        self.assertEqual(u'23', course_run['students_attended'])
        self.assertEqual(u'2', course_run['grade_12'])
        self.assertEqual(u'3', course_run['grade_10'])
        self.assertEqual(u'13', course_run['grade_7'])
        self.assertEqual(u'1', course_run['grade_4'])
        self.assertEqual(u'4', course_run['grade_02'])
        self.assertEqual(u'0', course_run['grade_00'])
        self.assertEqual(u'0', course_run['grade_minus_3'])
