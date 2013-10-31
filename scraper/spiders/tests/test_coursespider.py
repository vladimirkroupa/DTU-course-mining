import unittest
import os
from scraper.spiders.coursespider import CourseSpider
from util.scrapy_testutils import fake_response_from_file
from scraper.spiders.tests import __file__ as test_directory
from scraper.items import DepartmentItem
from scraper.items import CourseItem

def data_dir():
    return os.path.join(os.path.dirname(test_directory), 'data')

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

    def test_parse_grade_dist_page(self):
        response = fake_response_from_file(self.course_27002_course_run_page)
        response.meta['course'] = CourseItem(course_runs = [], code = '27002')
        response.meta['total_grade_pages'] = 1
        courseItem = self.spider.course_run_parser.parse_grade_dist_page(response)
        course_run = courseItem['course_runs'][0]

        self.assertEqual(u'2010', course_run['year'])
        self.assertEqual(u'Summer', course_run['semester'])
        self.assertEqual(u'74', course_run['students_registered'])
        self.assertEqual(u'61', course_run['students_attended'])
        self.assertEqual(u'45', course_run['students_passed'])
        self.assertEqual(u'4.7', course_run['exam_average'])
        self.assertEqual(u'2', course_run['grade_12'])
        self.assertEqual(u'10', course_run['grade_10'])
        self.assertEqual(u'21', course_run['grade_7'])
        self.assertEqual(u'7', course_run['grade_4'])
        self.assertEqual(u'5', course_run['grade_02'])
        self.assertEqual(u'8', course_run['grade_00'])
        self.assertEqual(u'8', course_run['grade_minus_3'])
        self.assertEqual(u'2', course_run['sick'])
        self.assertEqual(u'11', course_run['not_shown'])

    def test_parse_evaluation_page(self):
        response = fake_response_from_file(self.course_27002_evaluation_page)
        response.meta['course'] = CourseItem()
        response.meta['total_eval_pages'] = 1
        self.spider.parse_evaluation_page(response)

        pass