from scrapy.selector import HtmlXPathSelector
from util.scrapy_utils import *
from scraper.items import CourseRun
from collections import defaultdict
import logging
import re

class CourseRunParser():

    def __init__(self, log):
        self.log = log

    def parse_grade_dist_page(self, response):
        course = response.request.meta['course']
        hxs = HtmlXPathSelector(response)
        grades_table = select_single(hxs, '//table[2]')
        h2_value = select_single(hxs, '//form[@id="karsumForm"]/h2/text()').extract().strip().encode('utf-8')

        course_run = CourseRun()
        self.process_grade_table(grades_table, course_run)
        self.process_course_run_heading(h2_value, course_run)

        course['course_runs'].append(course_run)

        course_code = course['code']

        page_counter = response.request.meta['counter']
        page_counter.count_grade_page(course_code)
        if page_counter.course_processed(course_code):
            return course

    def process_grade_table(self, grades_table, course_run):

        def has_13_grades(grades_table):
            tables = grades_table.select('tr/td/table')
            return len(tables) == 2

        def not_enough_grades(grades_table):
            xpath = 'tr/td/text()[contains(., "Fordelingen vises ikke da tre eller")]'
            result = grades_table.select(xpath)
            return len(result) == 1

        def process_grade_table_line(header, value, course_run):
            item_fields = {'12' : 'grade_12',
                           '10': 'grade_10',
                           '7': 'grade_7',
                           '4': 'grade_4',
                           '02': 'grade_02',
                           '00': 'grade_00',
                           '-3': 'grade_minus_3',
                           'Ill': 'sick',
                           'No show': 'not_shown'}

            if header not in item_fields:
                self.log('Grade table contains unexpected header {}'.format(header), level=logging.ERROR)
            field = item_fields[header]
            course_run[field] = value
            #self.log('Extracted occurrence of grade {}: {}'.format(header, value))

        if not_enough_grades(grades_table):
            self.log('Encountered course run with no grade distribution.')
            return

        if has_13_grades(grades_table):
            self.log('Encountered course run with 13 grade distribution.')
            return

        inner_table = select_single(grades_table, 'tr/td/table')
        for row in inner_table.select('tr')[1:]:
            header = select_single(row, 'td[1]/text()').extract().strip().encode('utf-8')
            value = select_single(row, 'td[2]/text()').extract().strip().encode('utf-8')
            process_grade_table_line(header, value, course_run)

    def process_course_run_heading(self, heading_text, course_run):
        self.log('Going to parse course run heading: [{}]'.format(heading_text))
        regex = re.compile("""(?:.*)(Summer|Winter)\s(\d\d\d\d)$""")
        match = regex.match(heading_text)
        groups = match.groups()
        check_len(groups, 2)
        semester, year = groups
        course_run['year'] = year
        course_run['semester'] = semester

    def process_course_run_info(self, grade):
        pass