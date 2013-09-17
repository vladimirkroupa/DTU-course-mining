# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CourseItem(Item):
    code = Field()
    title_en = Field()
    title_da = Field()
    evaluation = Field()
    ects_credits = Field()
