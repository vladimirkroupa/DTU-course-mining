class CourseRun:

    def __init__(self):
        self.year = None
        # semesters + 3 week period: E, F, June, January
        self.semester = None
        self.students_registered = 0
        self.students_attended = 0
        self.students_passed = 0
        self._exam_average = 0.0
        self.grade_scale = {'12' : 0,
                            '10' : 0,
                            '7' : 0,
                            '4' : 0,
                            '02' : 0,
                            '00' : 0,
                            '-3' : 0}
        self.not_shown = 0
        self.sick = 0

    def exam_average(self):
        pass