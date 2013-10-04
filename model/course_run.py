class CourseRun:

    def __init__(self, year, semester, students_registered, students_attended, students_passed, not_shown, sick, grade_scale):
        self.year = year
        # semesters + 3 week period: E, F, June, January
        self.semester = semester
        self.students_registered = students_registered
        self.students_attended = students_attended
        self.students_passed = students_passed
        self.grade_scale = grade_scale
        self.not_shown = not_shown
        self.sick = sick

    def exam_average(self):
        pass

    def __repr__(self):
        templ = "Course run on {} semester {}: {} registered, {} attended, {} passed, {} not shown, {} sick, grade scale: {}"
        return templ.format(self.semester, self.year, self.students_registered, self.students_attended, self.students_passed,
                            self.not_shown, self.sick, self.grade_scale)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        assert False, '__eq__ implementation required!'