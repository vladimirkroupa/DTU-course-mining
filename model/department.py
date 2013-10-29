import operator

class Department:

    def __init__(self, code, title_en, title_da, courses = None):
        self.code = code
        self.name_en = title_en
        self.name_da = title_da
        if courses is None:
            self.courses = []

    def add_course(self, course):
        self.courses.append(course)
        course.department = self

    def __repr__(self):
        templ = u"{} : {} ({})"
        result = templ.format(self.code, self.name_en, self.name_da)
        return result.encode("utf-8")

    def __str__(self):
        return self.__repr__()

    def __key__(self):
        return (self.code, self.name_en, self.name_da)

    def __eq__(self, other):
        comparisons = [
            self.code == other.code,
            self.name_en == other.name_en,
            self.name_da == other.name_da
        ]
        return reduce(operator.and_, comparisons)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key__())
