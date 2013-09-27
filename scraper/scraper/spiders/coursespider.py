from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urlparse import urljoin
import re
from scraper.items import CourseItem
from scraper.items import CourseRun
import logging

#TODO: need to move out everything except the class itself

class PageStructureException(Exception):
    pass


def select_single(selector, xpath):
    return select(selector, xpath, expected = 1)[0]

def select(selector, xpath, expected = None):
    result = selector.select(xpath)
    if expected is not None and len(result) != expected:
        msg = "Expected {0} result(s), got {1}. XPath expression: {2} Selector content: {3}".format(expected, len(result), xpath, selector.extract())
        raise PageStructureException(msg)
    return result

def check_len(list, item_count):
    if len(list) != item_count:
        raise PageStructureException("Expected {0} element(s), got: {1}").format(len(list))

def single_elem(list):
    check_len(list, 1)
    return list[0]


class CourseSpider(BaseSpider):
    name = 'CourseSpider'
    allowed_domains = ['dtu.dk']
    start_urls = ['http://www.kurser.dtu.dk/2013-2014/index.aspx']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        base_url = get_base_url(response)
        self.log("Base URL: " + base_url)
        for rel_path in hxs.select('(//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id]/td/lu/li/a/@href)[1]').extract():
        #for rel_path in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id]/td/lu/li/a/@href').extract():
            department_url = urljoin(base_url, rel_path)
            self.log("Extracted department URL: " + department_url)
            yield Request(department_url, callback = self.parse_department)

    def parse_department(self, response):
        base_url = get_base_url(response)
        hxs = HtmlXPathSelector(response)
        for onclick in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr[2]/td/table/tr[@id]/@onclick'):
            course_url = self.extract_course_url(onclick, base_url)
            self.log("Extracted course URL: " + course_url)
            course_url_en = course_url + '?menulanguage=en-GB'
            yield Request(course_url_en, callback = self.parse_course)

    def extract_course_url(self, onclick, base_url):
        regex = "(?:document.location=')(.*)(?:')"
        course_relpath = single_elem(onclick.re(regex))
        return urljoin(base_url, course_relpath)

    def parse_course(self, response):
        hxs = HtmlXPathSelector(response)
        main_div = select_single(hxs, '//div[@class = "CourseViewer"]/div[@id = "pagecontents"]')
        course = CourseItem()
        self.process_heading(main_div, course)
        self.process_first_table(main_div, course)
        self.process_second_table(main_div, course)
        eval_url = self.create_course_eval_request(response.url)
        yield Request(eval_url, callback = self.parse_page_with_info_link)

    def create_course_eval_request(self, course_url):
        tokens = course_url.split("/")
        del tokens[-2] # delete second last
        return "/".join(tokens)

    def process_heading(self, main_div, course):
        h2 = select_single(main_div, 'h2/text()').extract().strip()
        self.log('Extracted course code and title: ' + h2)
        regex = re.compile('^([0-9A-Z]{5}) (.*)')
        match = regex.match(h2)
        code_en_name = match.groups()
        check_len(code_en_name, 2)

        course['code'] = code_en_name[0]
        course['title_en'] = code_en_name[1]

    def process_table_row(self, table, heading, text_nodes_handler = lambda vals : vals[0].strip(), postprocess = None):
        xpath = 'tr[contains(td/h3/text(), "{}")]'.format(heading)
        table_row = select_single(table, xpath)
        # finds all text values in the column
        line_values = table_row.select('td[2]/descendant::text()').extract()
        #
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
        return Request(url, callback = self.parse_grade_overview_page)

    def parse_grade_overview_page(self, response):
        hxs = HtmlXPathSelector(response)
        grades_table = select_single(hxs, '//td[@class = "ContentMain"]//table[contains(tr/td/b/text(), "Grades")]')
        grade_links = grades_table.select('tr[2]/td[2]/a/@href').extract()
        for link in grade_links:
            yield Request(link, callback = self.parse_grade_dist_page)

    def parse_grade_dist_page(self, response):

        def process_grade_table_line(header, value, course_run):
            item_fields = {'12' : 'grade_12',
                           '10': 'grade_10',
                           '7': 'grade_7',
                           '4': 'grade_4',
                           '02': 'grade_02',
                           '00': 'grade_00',
                           '-3': 'grade_minus_3',
                           'Syg': 'sick'}
                           #'Ej mødt': 'not_shown'}

            if header not in item_fields:
                self.log('Grade table contains unexpected header {}'.format(header), level=logging.ERROR)
            field = item_fields[header]
            course_run[field] = value
            self.log('Extracted occurrence of grade {0}: {1}'.format(header, value))

        course_run = CourseRun()
        hxs = HtmlXPathSelector(response)
        grades_table = select_single(hxs, '//table[3]')
        for row in grades_table.select('tr')[1:]:
            header = select_single(row, 'td[1]/text()').extract().strip()
            value = select_single(row, 'td[2]/text()').extract().strip()
            process_grade_table_line(header, value, course_run)
            yield course_run