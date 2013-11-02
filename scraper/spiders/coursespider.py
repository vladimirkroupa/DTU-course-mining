# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urlparse import urljoin
import re
from scraper.items import CourseItem
from scraper.items import DepartmentItem
from util.scrapy_utils import *
from course_run_parser import CourseRunParser
from page_counter import PageCounter

class CourseSpider(BaseSpider):
    name = 'CourseSpider'
    allowed_domains = ['dtu.dk']
    start_urls = ['http://www.kurser.dtu.dk/2013-2014/index.aspx?menulanguage=en-GB']

    def __init__(self):
        self.course_run_parser = CourseRunParser(self.log)

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
        return Request(url, callback = self.parse_course_information_page, meta = {'course' : course})

    def parse_course_information_page(self, response):
        hxs = HtmlXPathSelector(response)
        course = response.meta['course']
        main_td = select_single(hxs, '//td[@class = "ContentMain"]')

        grades_table = select_single(main_td, '//table[contains(tr/td/b/text(), "Grades")]')
        grade_links = grades_table.select('tr[2]/td[2]/a/@href').extract()

        evaluations_table = select_single(main_td, '//table[contains(tr/td/b/text(), "Course evaluations")]')
        eval_links = evaluations_table.select('tr/td/a/@href').extract()

        page_counter = PageCounter(total_grade_pages = len(grade_links),
                                   total_evaluation_pages = len(eval_links),
                                   log = self.log)

        for link in grade_links:
            request = Request(link, callback = self.course_run_parser.parse_grade_dist_page, meta = {'course' : course, 'counter' : page_counter})
            yield request

        for link in eval_links:
            request = Request(link, callback = self.parse_evaluation_page, meta = {'course' : course, 'counter' : page_counter})
            yield request

    def parse_evaluation_page(self, response):
        course = response.request.meta['course']
        hxs = HtmlXPathSelector(response)

        stats_table = select_single(hxs, '//table[contains(tr/td/text(), "Statistics")]')
        could_answer = select_single(stats_table, 'tr[contains(td/text(), "could answer this evaluation form")]/td[1]/b/text()')
        have_answered = select_single(stats_table, 'tr[contains(td/text(), "have answered this evaluation form")]/td[1]/b/text()')
        did_not_follow = select_single(stats_table, 'tr[contains(td/text(), "did not follow the course")]/td[1]/b/text()')
        answers_table = select_single(hxs, '//form/table[2]')

        self.parse_answers_table(answers_table, course)

        #TODO: (//form/table[2]/tbody/tr[contains(td/em/text(), "I think the course description’s prerequisites are")]/following-sibling::tr[count(child::td) = 4]/td[4])

        pass

    def parse_answers_table(self, table, course):

        xpath_templ = 'tr[contains(td/em/text(), "{}")]'
        nth_xpath = '(following-sibling::tr[count(child::td) = 4]/td[3]/text())[{}]'

        def parse_question(table, question_text):
            xpath = xpath_templ.format(question_text)
            question_row = select_single(table, xpath)
            answer_1 = select_single(question_row, nth_xpath.format(1)).extract()
            answer_2 = select_single(question_row, nth_xpath.format(2)).extract()
            answer_3  = select_single(question_row, nth_xpath.format(3)).extract()
            answer_4 = select_single(question_row, nth_xpath.format(4)).extract()
            answer_5 = select_single(question_row, nth_xpath.format(5)).extract()
            return (answer_1, answer_2, answer_3, answer_4, answer_5)

        def parse_workload_question(table):
            return parse_question(table, 'I think my performance during the course is')

        def parse_prereq_question(table):
            return parse_question(table, 'I think the course description')

        workload_answers = parse_workload_question(table)
        
        prereq_anwers = parse_prereq_question(table)

        print workload_answers

        print prereq_anwers


