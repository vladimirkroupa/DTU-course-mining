from scrapy import log
from scraper.items import CourseItem
from storage.course_repository import CourseRepository

class RepositoryPipeline(object):

    def __init__(self):
        self.repository = CourseRepository('sqlite:///courses.db')

    def process_item(self, item, spider):
        if isinstance(item, CourseItem):
            self.repository.store_course_item(item)
        else:
            raise ValueError("Unexpected item type " + type(item))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
