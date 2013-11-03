import unittest
import os
from scraper.spiders.evaluation_parser import EvaluationParser
from util.scrapy_testutils import fake_response_from_file
from scraper.spiders.tests import __file__ as test_directory
from scraper.items import CourseItem
from scraper.spiders.page_counter import PageCounter

def data_dir():
    return os.path.join(os.path.dirname(test_directory), 'data')

class CourseEvaluationParserTest(unittest.TestCase):

    def setUp(self):
        self.evaluation_parser = EvaluationParser(log = None)
        self.course_27002_evaluation_page = os.path.join(data_dir(), '27002_evaluation.html')
        self.evaluation_did_not_follow_missing = os.path.join(data_dir(), 'Evaluation_no_dnf.html')
        self.evaluation_3_week_course = os.path.join(data_dir(), 'Evaluation_3_week_course.html')


    def test_parse_evaluation_page(self):
        response = fake_response_from_file(self.course_27002_evaluation_page)
        response.meta['course'] = CourseItem(evaluations = [], code = '27002')
        response.meta['counter'] = PageCounter(0, 1)

        course_item = self.evaluation_parser.parse_evaluation_page(response)
        evaluation = course_item['evaluations'][0]

        self.assertEqual(u'2011', evaluation['year'])
        self.assertEqual(u'Summer', evaluation['semester'])
        self.assertEqual(u'80', evaluation['could_answer'])
        self.assertEqual(u'40', evaluation['have_answered'])
        self.assertEqual(u'6', evaluation['did_not_follow'])

        self.assertEqual(u'5', evaluation['performance_much_less'])
        self.assertEqual(u'9', evaluation['performance_less'])
        self.assertEqual(u'26', evaluation['performance_same'])
        self.assertEqual(u'0', evaluation['performance_more'])
        self.assertEqual(u'0', evaluation['performance_much_more'])

        self.assertEqual(u'0', evaluation['prereq_too_low'])
        self.assertEqual(u'2', evaluation['prereq_low'])
        self.assertEqual(u'36', evaluation['prereq_adequate'])
        self.assertEqual(u'1', evaluation['prereq_high'])
        self.assertEqual(u'1', evaluation['prereq_too_high'])

    def test_parse_evaluation_page_missing_dnf(self):
        response = fake_response_from_file(self.evaluation_did_not_follow_missing)
        response.meta['course'] = CourseItem(evaluations = [], code = '11124')
        response.meta['counter'] = PageCounter(0, 1)

        course_item = self.evaluation_parser.parse_evaluation_page(response)
        evaluation = course_item['evaluations'][0]

        self.assertEqual(u'2008', evaluation['year'])
        self.assertEqual(u'Winter', evaluation['semester'])
        self.assertEqual(u'24', evaluation['could_answer'])
        self.assertEqual(u'15', evaluation['have_answered'])
        self.assertEqual(u'0', evaluation['did_not_follow'])

        self.assertEqual(u'0', evaluation['performance_much_less'])
        self.assertEqual(u'0', evaluation['performance_less'])
        self.assertEqual(u'11', evaluation['performance_same'])
        self.assertEqual(u'4', evaluation['performance_more'])
        self.assertEqual(u'0', evaluation['performance_much_more'])

        self.assertEqual(u'0', evaluation['prereq_too_low'])
        self.assertEqual(u'2', evaluation['prereq_low'])
        self.assertEqual(u'10', evaluation['prereq_adequate'])
        self.assertEqual(u'2', evaluation['prereq_high'])
        self.assertEqual(u'0', evaluation['prereq_too_high'])

    def test_parse_evaluation_3_week_period_course(self):
        response = fake_response_from_file(self.evaluation_3_week_course)
        response.meta['course'] = CourseItem(evaluations = [], code = '11126')
        response.meta['counter'] = PageCounter(0, 1)

        course_item = self.evaluation_parser.parse_evaluation_page(response)
        evaluation = course_item['evaluations'][0]

        self.assertEqual(u'2009', evaluation['year'])
        self.assertEqual(u'January', evaluation['semester'])
        self.assertEqual(u'7', evaluation['could_answer'])
        self.assertEqual(u'4', evaluation['have_answered'])
        self.assertEqual(u'0', evaluation['did_not_follow'])

        self.assertEqual(u'0', evaluation['performance_much_less'])
        self.assertEqual(u'1', evaluation['performance_less'])
        self.assertEqual(u'3', evaluation['performance_same'])
        self.assertEqual(u'0', evaluation['performance_more'])
        self.assertEqual(u'0', evaluation['performance_much_more'])

        self.assertEqual(u'0', evaluation['prereq_too_low'])
        self.assertEqual(u'0', evaluation['prereq_low'])
        self.assertEqual(u'4', evaluation['prereq_adequate'])
        self.assertEqual(u'0', evaluation['prereq_high'])
        self.assertEqual(u'0', evaluation['prereq_too_high'])