import operator

class CourseRun:

    def __init__(self, year, semester, students_registered, students_attended, students_passed, not_shown, sick, grade_scale):

        self.grade_scale = {}

        def init_grade_scale(self, grade_scale):
            self.grade_scale['12'] = grade_scale.get('12', 0)
            self.grade_scale['10'] = grade_scale.get('10', 0)
            self.grade_scale['7'] = grade_scale.get('7', 0)
            self.grade_scale['4'] = grade_scale.get('4', 0)
            self.grade_scale['02'] = grade_scale.get('02', 0)
            self.grade_scale['00'] = grade_scale.get('00', 0)
            self.grade_scale['-3'] = grade_scale.get('-3', 0)

        self.year = year
        # semesters + 3 week period: E, F, June, January
        self.semester = semester
        self.students_registered = students_registered
        self.students_attended = students_attended
        self.students_passed = students_passed
        self.not_shown = not_shown
        self.sick = sick
        init_grade_scale(self, grade_scale)

    def exam_average(self):
        pass

    def __key__(self):
        return (self.year, self.semester, self.students_registered, self.students_attended, self.students_passed, self.not_shown, self.sick, frozenset(self.grade_scale.items()))

    def __repr__(self):
        templ = "Course run on {} semester {}: {} registered, {} attended, {} passed, {} not shown, {} sick, grade scale: {}"
        return templ.format(self.semester, self.year, self.students_registered, self.students_attended, self.students_passed,
                            self.not_shown, self.sick, self.grade_scale)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        comparisons = [
            self.year == other.year,
            self.semester == other.semester,
            self.students_registered == other.students_registered,
            self.students_attended == other.students_attended,
            self.students_passed == other.students_passed,
            self.not_shown == other.not_shown,
            self.sick == other.sick,
            self.grade_scale == other.grade_scale
        ]
        return reduce(operator.and_, comparisons)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key__())