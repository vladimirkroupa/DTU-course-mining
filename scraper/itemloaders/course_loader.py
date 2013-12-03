from scrapy.contrib.loader import XPathItemLoader
from scraper.items import CourseItem
from scraper.itemloaders.processors import EvaluationTypeProcessor, Strip, ParseCommaFloat
from scrapy.contrib.loader.processor import TakeFirst, Identity

class CourseItemLoader(XPathItemLoader):

    default_item_class = CourseItem

    default_input_processor = Strip()
    default_output_processor = TakeFirst()

    title_da_in = Strip()
    evaluation_type_in = EvaluationTypeProcessor()
    ects_credits_in = ParseCommaFloat()

    previous_out = Identity()
    prereqs_out = Identity()

    def __init__(self, response):
        super(CourseItemLoader, self).__init__(response=response)

        MAIN_DIV = '//div[@class = "CourseViewer"]/div[@id = "pagecontents"]'
        self.add_xpath('code', MAIN_DIV + '/h2/text()', re = r'([0-9A-Z]{5})')
        self.add_xpath('title_en', MAIN_DIV + '/h2/text()', re = r'[0-9A-Z]{5} (.*)')

        TABLE_1_ROW = MAIN_DIV + '/table[1]/tr[contains(td/h3/text(), "{}")]/td[2]/descendant::text()'
        self.add_xpath('language', TABLE_1_ROW.format('Language:'))
        self.add_xpath('title_da', TABLE_1_ROW.format('Danish title:'))
        self.add_xpath('ects_credits', TABLE_1_ROW.format('Point( ECTS )'))
        self.add_xpath('course_type', TABLE_1_ROW.format('Course type:'))

        TABLE_2_ROW = MAIN_DIV + '/table[2]/tr[contains(td/h3/text(), "{}")]/td[2]/descendant::text()'
        self.add_xpath('evaluation_type', TABLE_2_ROW.format('Evaluation:'))
        self.add_xpath('prereqs', TABLE_2_ROW.format('Qualified Prerequisites:'))
        self.add_xpath('previous', TABLE_2_ROW.format('Previous Course:'))