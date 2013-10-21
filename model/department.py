import operator
from storage.static_storage import StaticStorage

class Department:

    def __init__(self, code, title_en, title_da):
        self.code = code
        self.name_en = title_en
        self.name_da = title_da
        self.storage = StaticStorage()

    def courses(self):
        return self.storage.find_department_by_code(self.code)

    def __repr__(self):
        templ = "{} : {} ({})"
        return templ.format(self.code, self.name_en, self.name_da)

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

    def __hash__(self):
        return hash(self.__key__())
