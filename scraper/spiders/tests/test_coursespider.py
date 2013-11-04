import unittest
import os
from scraper.spiders.coursespider import CourseSpider
from util.scrapy_testutils import fake_response_from_file
from scraper.spiders.tests import __file__ as test_directory
from scraper.items import DepartmentItem
from scraper.items import CourseItem
from scraper.spiders.tests.data import data_dir

class CourseSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = CourseSpider()
        self.department_list_page = os.path.join(data_dir(), 'DTU_Coursebase.html')
        self.department_27_page = os.path.join(data_dir(), 'Department27.html')
        self.course_27002_page = os.path.join(data_dir(), '27002.html')
        self.course_27002_info_page = os.path.join(data_dir(), '27002_information.html')
        self.course_27002_course_run_page = os.path.join(data_dir(), '27002_course_run_summer_2010.html')
        self.course_27002_evaluation_page = os.path.join(data_dir(), '27002_evaluation.html')

    def _check_departments(self, results):
        expected = [
            DepartmentItem(code = '27', title_en = 'Department of Systems Biology'),
            DepartmentItem(code = '11', title_en = 'Department of Civil Engineering'),
        ]
        departments = [item.meta['department'] for item in results]
        self.assertEqual(expected, departments)

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file(self.department_list_page))
        result_list = list(results)
        self.assertTrue(len(result_list) == 2)
        self._check_departments(result_list)

    def test_parse_department_page(self):
        response = fake_response_from_file(self.department_27_page)
        response.meta['department'] = DepartmentItem()
        results = self.spider.parse_department_page(response)
        result_list = list(results)
        self.assertEqual(len(result_list), 64)

    def test_parse_course(self):
        response = fake_response_from_file(self.course_27002_page)
        response.meta['department'] = DepartmentItem()
        results = self.spider.parse_course(response)
        actual = results.next().meta['course']

        self.assertEqual(u'27002', actual['code'])
        self.assertEqual(u'Danish', actual['language'])
        self.assertEqual(u'Life Science', actual['title_en'])
        self.assertEqual(u'Biovidenskab', actual['title_da'])
        self.assertEqual(u'7 step scale', actual['evaluation_type'])
        self.assertEqual(u'5', actual['ects_credits'])
        self.assertEqual(u'BSc', actual['course_type'])

    def test_parse_course_information_page(self):
        response = fake_response_from_file(self.course_27002_info_page)
        response.meta['course'] = CourseItem()
        response.meta['department'] = DepartmentItem()
        results = self.spider.parse_course_information_page(response)
        self.assertEqual(len(list(results)), 17 + 5)
