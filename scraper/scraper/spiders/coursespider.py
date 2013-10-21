# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urlparse import urljoin
import re
from scraper.items import CourseItem
from scraper.items import CourseRun
from scraper.items import DepartmentItem
import logging
from collections import defaultdict

#TODO: need to move out everything except the class itself

class PageStructureException(Exception):
    pass


def select_single(selector, xpath):
    return select(selector, xpath, expected = 1)[0]

def select(selector, xpath, expected = None):
    result = selector.select(xpath)
    if expected is not None and len(result) != expected:
        msg = "Expected {0} result(s), got {1}. XPath expression: {2} Selector content: {3}".format(expected, len(result), xpath, selector.extract().encode('utf-8'))
        raise PageStructureException(msg)
    return result

def check_len(list, item_count):
    if len(list) != item_count:
        raise PageStructureException("Expected {0} element(s), got: {1}".format(item_count, len(list)))
    return list

def single_elem(list):
    check_len(list, 1)
    return list[0]


class CourseSpider(BaseSpider):
    name = 'CourseSpider'
    allowed_domains = ['dtu.dk']
    start_urls = ['http://www.kurser.dtu.dk/2013-2014/index.aspx?menulanguage=en-GB']
    course_grades_parsed = defaultdict(int)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        base_url = get_base_url(response)
        self.log("Base URL: " + base_url)
        #for department_line in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id]'):
        for department_line in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id][1] | //div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id][2]'):
            department = self.parse_department(department_line)
            department_url = self.extract_department_link(base_url, department_line)
            yield Request(department_url, callback = self.parse_department_page, meta = {'department' : department})

    def parse_department(self, department_line):
        line_text = select_single(department_line, 'td/lu/li/a/text()').extract().strip().encode('utf-8')
        regex = re.compile('([0-9]+) ([\w\s]+)')
        match = regex.match(line_text)
        groups = match.groups()
        check_len(groups, 2)
        code, title_en = groups
        department = DepartmentItem()
        department['code'] = code
        department['title_en'] = title_en
        return department

    def extract_department_link(self, base_url, department_line):
        rel_path = select_single(department_line, 'td/lu/li/a/@href').extract()
        department_url = urljoin(base_url, rel_path)
        self.log("Extracted department URL: " + department_url)
        return department_url

    def parse_department_page(self, response):
        department = response.meta['department']
        base_url = get_base_url(response)
        hxs = HtmlXPathSelector(response)
        for onclick in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr[2]/td/table/tr[@id]/@onclick'):
            course_url = self.extract_course_url(onclick, base_url)
            self.log("Extracted course URL: " + course_url)
            course_url_en = course_url + '?menulanguage=en-GB'
            yield Request(course_url_en, callback = self.parse_course, meta = {'department' : department})

    def extract_course_url(self, onclick, base_url):
        regex = "(?:document.location=')(.*)(?:')"
        course_relpath = single_elem(onclick.re(regex))
        return urljoin(base_url, course_relpath)

    def parse_course(self, response):
        department = response.meta['department']
        hxs = HtmlXPathSelector(response)
        main_div = select_single(hxs, '//div[@class = "CourseViewer"]/div[@id = "pagecontents"]')
        course = CourseItem(course_runs = [], department = department)
        self.process_heading(main_div, course)
        self.process_first_table(main_div, course)
        self.process_second_table(main_div, course)
        eval_url = self.create_course_eval_request(response.url)

        # TODO: move to Course class
        if course['evaluation_type'] == 'pass / not pass':
            self.log('Skipping pass/fail evaluation type course {}'.format(course['title_en']))
            return

        yield Request(eval_url, callback = self.parse_page_with_info_link, meta = {'course' : course})

    def create_course_eval_request(self, course_url):
        tokens = course_url.split("/")
        del tokens[-2] # delete second last
        return "/".join(tokens)

    def process_heading(self, main_div, course):
        h2 = select_single(main_div, 'h2/text()').extract().strip()
        self.log('Going to parse course code and title: ' + h2)
        regex = re.compile('^([0-9A-Z]{5}) (.*)')
        match = regex.match(h2)
        groups = match.groups()
        check_len(groups, 2)
        code, en_name = groups

        course['code'] = code
        course['title_en'] = en_name

    def process_table_row(self, table, heading, text_nodes_handler = lambda vals : vals[0].strip(), postprocess = None):
        xpath = 'tr[contains(td/h3/text(), "{}")]'.format(heading)
        table_row = select_single(table, xpath)
        # finds all text values in the column
        line_values = [s.encode('utf-8') for s in table_row.select('td[2]/descendant::text()').extract()]
        result = text_nodes_handler(line_values)
        if postprocess:
            result = postprocess(result)
        self.log("Extracted '{}' value: '{}'".format(heading, result))
        return result

    def process_first_table(self, main_div, course):

        table = main_div.select('table[1]')

        course['title_da'] = self.process_table_row(table, "Danish title:")

        course['language'] = self.process_table_row(table, "Language:")

        course['ects_credits'] = self.process_table_row(table, "Point( ECTS )")

        course['course_type'] = self.process_table_row(table, "Course type:")

    def process_second_table(self, main_div, course):

        def parse_evaluation_type(eval_type_string):
            return eval_type_string.split(',')[0].strip()

        table = main_div.select('table[2]')
        eval_type = self.process_table_row(table, "Evaluation:", postprocess = parse_evaluation_type)
        course['evaluation_type'] = eval_type

    def parse_page_with_info_link(self, response):
        hxs = HtmlXPathSelector(response)
        base_url = get_base_url(response)
        href = select_single(hxs, '//tr[@class = "tabNavigation"]//a[text() = "Information"]/@href').extract()
        url = urljoin(base_url, href)
        course = response.meta['course']
        return Request(url, callback = self.parse_grade_overview_page, meta = {'course' : course})

    def parse_grade_overview_page(self, response):
        hxs = HtmlXPathSelector(response)
        grades_table = select_single(hxs, '//td[@class = "ContentMain"]//table[contains(tr/td/b/text(), "Grades")]')
        grade_links = grades_table.select('tr[2]/td[2]/a/@href').extract()
        page_no = 0
        for link in grade_links:
            page_no += 1
            course = response.meta['course']
            yield Request(link, callback = self.parse_grade_dist_page, meta = {'course' : course, 'total_grade_pages' : len(grade_links)})

    def parse_grade_dist_page(self, response):
        course = response.request.meta['course']
        hxs = HtmlXPathSelector(response)
        grades_table = select_single(hxs, '//table[2]')
        h2_value = select_single(hxs, '//form[@id="karsumForm"]/h2/text()').extract().strip().encode('utf-8')

        course_run = CourseRun()
        self.process_grade_table(grades_table, course_run)
        self.process_course_run_heading(h2_value, course_run)

        self.log(course_run)
        course['course_runs'].append(course_run)

        course_code = course['code']
        self.course_grades_parsed[course_code] += 1

        pages_parsed = self.course_grades_parsed[course_code]
        total_pages = response.meta['total_grade_pages']
        self.log("Scraped {} grade pages of {} total for course {}.".format(pages_parsed, total_pages, course_code))
        if pages_parsed == total_pages:
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
                           'Syg': 'sick',
                           'Ej mødt': 'not_shown'}

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
        regex = re.compile("""(?:.*)(Sommer|Vinter)\s(\d\d\d\d)$""")
        match = regex.match(heading_text)
        groups = match.groups()
        check_len(groups, 2)
        semester, year = groups
        course_run['year'] = year
        course_run['semester'] = semester

    def process_course_run_info(self, grade):
        pass
