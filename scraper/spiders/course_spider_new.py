from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urlparse import urljoin
from util.scrapy_utils import *
from scraper.itemloaders.course_loader import CourseItemLoader
from scraper.itemloaders.department_loader import DepartmentItemLoader

class CourseSpiderNew(BaseSpider):
    name = 'CourseSpiderNew'
    allowed_domains = ['dtu.dk']
    start_urls = ['http://www.kurser.dtu.dk/2013-2014/index.aspx?menulanguage=en-GB']

    def parse(self, response):
        hxs = Selector(response)
        base_url = get_base_url(response)
        self.log("Base URL: " + base_url)
        for department_line in hxs.select('//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id]'):
        #for department_line in hxs.xpath('//div[@class = "CourseViewer"]/table/tr/td/table/tr/td/table/tr[@id][1]'):
            department = self.parse_department(department_line)
            department_url = self.extract_department_link(base_url, department_line)
            yield Request(department_url, callback = self.parse_department_page, meta = {'department' : department})

    def parse_department(self, department_line):
        l = DepartmentItemLoader(department_line)
        return l.load_item()

    def extract_department_link(self, base_url, department_line):
        rel_path = select_single(department_line, 'td/lu/li/a/@href').extract()
        department_url = urljoin(base_url, rel_path)
        self.log("Extracted department URL: " + department_url)
        return department_url

    def parse_department_page(self, response):
        department = response.meta['department']
        base_url = get_base_url(response)
        hxs = Selector(response)
        for onclick in hxs.xpath('//div[@class = "CourseViewer"]/table/tr/td/table/tr[2]/td/table/tr[@id]/@onclick'):
            course_url = self.extract_course_url(onclick, base_url)
            self.log("Extracted course URL: " + course_url)
            course_url_en = set_url_param(course_url, 'menulanguage', 'en-GB')
            yield Request(course_url_en, callback = self.parse_course, meta = {'department' : department})

    def extract_course_url(self, onclick, base_url):
        regex = "(?:document.location=')(.*)(?:')"
        course_relpath = single_elem(onclick.re(regex))
        return urljoin(base_url, course_relpath)

    def parse_course(self, response):
        department = response.meta['department']
        l = CourseItemLoader(response)
        course = l.load_item()
        course['department'] = department
        return course
