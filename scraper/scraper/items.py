from scrapy.item import Item, Field

class CourseItem(Item):
    """
    TODO
    """

    code = Field()
    language = Field()
    title_en = Field()
    title_da = Field()
    evaluation = Field()
    ects_credits = Field()
    course_type = Field()