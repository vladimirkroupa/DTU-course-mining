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
    evaluations = Field()
    prereqs = Field()
    prereq_desc = Field()
    previous = Field()

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
    grade_7 = Field()
    grade_4 = Field()
    grade_02 = Field()
    grade_00 = Field()
    grade_minus_3 = Field()
    not_shown = Field()
    sick = Field()

class EvaluationItem(Item):
    year = Field()
    # semesters + 3 week period: E, F, June, January
    semester = Field()
    could_answer = Field()
    have_answered = Field()
    did_not_follow = Field()

    performance_much_less = Field()
    performance_less = Field()
    performance_same = Field()
    performance_more = Field()
    performance_much_more = Field()

    prereq_too_low = Field()
    prereq_low = Field()
    prereq_adequate = Field()
    prereq_high = Field()
    prereq_too_high = Field()
