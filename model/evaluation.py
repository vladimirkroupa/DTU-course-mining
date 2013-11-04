import operator

class Evaluation():

    def __init__(self, year, semester, could_answer, have_answered, did_not_follow, performance_scale, prereq_scale):

        def convert_performance_scale(self, performance_scale):
            self.performance_intensity[1] = performance_scale.get('performance_much_less', 0)
            self.performance_intensity[2] = performance_scale.get('performance_less', 0)
            self.performance_intensity[3] = performance_scale.get('performance_same', 0)
            self.performance_intensity[4] = performance_scale.get('performance_more', 0)
            self.performance_intensity[5] = performance_scale.get('performance_much_more', 0)

        def convert_prereq_scale(self, prereq_scale):
            self.prereq_intensity[1] = prereq_scale.get('prereq_too_low', 0)
            self.prereq_intensity[2] = prereq_scale.get('prereq_low', 0)
            self.prereq_intensity[3] = prereq_scale.get('prereq_adequate', 0)
            self.prereq_intensity[4] = prereq_scale.get('prereq_high', 0)
            self.prereq_intensity[5] = prereq_scale.get('prereq_too_high', 0)

        self.year = year
        self.semester = semester
        self.could_answer = could_answer
        self.have_answered = have_answered
        self.did_not_follow = did_not_follow
        self.performance_intensity = {}
        self.prereq_intensity = {}
        convert_performance_scale(self, performance_scale)
        convert_prereq_scale(self, prereq_scale)

    def __key__(self):
        return (self.year, self.semester, self.could_answer, self.have_answered, self.did_not_follow, self.performance_intensity, self.prereq_intensity)

    def __repr__(self):
        templ = "Course evaluation from {}, {} semester: {} could answer, {} have answered, {} did not follow. Performance: {}, prerequisites: {}"
        return templ.format(self.year, self.semester, self.could_answer, self.have_answered, self.did_not_follow, self.performance_intensity, self.prereq_intensity)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        comparisons = [
            self.year == other.year,
            self.semester == other.semester,
            self.could_answer == other.could_answer,
            self.have_answered == other.have_answered,
            self.did_not_follow == other.did_not_follow,
            self.performance_intensity == other.performance_intensity,
            self.prereq_intensity == other.prereq_intesity
        ]
        return reduce(operator.and_, comparisons)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key__())