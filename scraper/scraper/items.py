from scrapy.item import Item, Field

class DepartmentItem(Item):
    code = Field()
    title_en = Field()
    title_da = Field()

class CourseItem(Item):
    """
    TODO
    """
    code = Field()
    language = Field()
    title_en = Field()
    title_da = Field()
    evaluation_type = Field()
    ects_credits = Field()
    course_type = Field()
    department = Field()
    course_runs = Field()

class CourseRun(Item):
    year = Field()
    # semesters + 3 week period: E, F, June, January
    semester = Field()
    students_registered = Field()
    students_attended = Field()
    students_passed = Field()
    exam_average = Field()
    grade_12 = Field()
    grade_10 = Field()
    grade_10 = Field()
    grade_7 = Field()
    grade_4 = Field()
    grade_02 = Field()
    grade_00 = Field()
    grade_minus_3 = Field()
    not_shown = Field()
    sick = Field()