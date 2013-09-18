from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urlparse import urljoin
import re
from scraper.items import CourseItem

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
        course_relpath = onclick.re(regex)
        assert len(course_relpath) == 1
        return urljoin(base_url, course_relpath[0])

    def parse_course(self, response):
        hxs = HtmlXPathSelector(response)
        main_div = hxs.select('//div[@class = "CourseViewer"]/div[@id = "pagecontents"]')

        h2 = main_div.select('h2/text()').extract()
        assert len(h2) == 1
        h2_str = h2[0].strip()
        self.log('Extracted course code and title: ' + h2_str)
        regex = re.compile('^([0-9A-Z]{5}) (.*)')
        match = regex.match(h2_str)
        code_en_name = match.groups()
        assert len(code_en_name) == 2

        item = CourseItem()
        item['code'] = code_en_name[0]
        item['title_en'] = code_en_name[1]

        #params_table = main_div.select('table[1]')
        #params_table
        return item