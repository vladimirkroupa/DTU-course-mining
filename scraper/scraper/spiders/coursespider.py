from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urlparse import urljoin
import re
from scraper.items import CourseItem

#TODO: need to move out everything except the class itself

class PageStructureException(Exception):
    pass


def select_single(selector, xpath, expected = None):
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
        for rel_path in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id]/td/lu/li/a/@href').extract():
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
        return course

    def process_heading(self, main_div, course):
        h2 = select_single(main_div, 'h2/text()').extract().strip()
        self.log('Extracted course code and title: ' + h2)
        regex = re.compile('^([0-9A-Z]{5}) (.*)')
        match = regex.match(h2)
        code_en_name = match.groups()
        check_len(code_en_name, 2)

        course['code'] = code_en_name[0]
        course['title_en'] = code_en_name[1]

    def process_table_row(self, table, row_no, expected_heading = None, values_handler = lambda vals : vals[0].strip()):
        xpath = 'tr[{}]'.format(row_no)
        line = select_single(table, xpath)
        line_header = select_single(line, 'td[1]/h3/text()').extract().strip()
        if expected_heading:
            assert line_header == expected_heading
        line_values = line.select('td[2]/descendant::text()').extract()
        result = values_handler(line_values)
        self.log("Extracted '{}' value: {}".format(expected_heading, result))
        return result

    def process_first_table(self, main_div, course):

        table = main_div.select('table[1]')

        course['title_da'] = self.process_table_row(table, 2, "Danish title:")

        course['language'] = self.process_table_row(table, 3, "Language:")

        course['ects_credits'] = self.process_table_row(table, 4, "Point( ECTS )")

        course['course_type'] = self.process_table_row(table, 5, "Course type:")

    def process_second_table(self, main_div, course):
        table = main_div.select('table[2]')
        pass