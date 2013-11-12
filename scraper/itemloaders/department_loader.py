from scrapy.contrib.loader import XPathItemLoader
from scraper.items import DepartmentItem
from scraper.itemloaders.processors import Strip
from scrapy.contrib.loader.processor import TakeFirst

class DepartmentItemLoader(XPathItemLoader):

    default_item_class = DepartmentItem

    default_input_processor = Strip()
    default_output_processor = TakeFirst()

    def __init__(self, dep_line_selector):
        super(DepartmentItemLoader, self).__init__(selector=dep_line_selector)

        self.add_xpath('code', 'td/lu/li/a/text()', re = r'([0-9]+) [\w\s]+')
        self.add_xpath('title_en', 'td/lu/li/a/text()', re = r'[0-9]+ ([\w\s]+)')

