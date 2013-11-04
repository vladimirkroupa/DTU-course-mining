import operator

class Evaluation():

    def __init__(self, year, semester, could_answer, have_answered, did_not_follow, performance_scale, prereq_scale):
        self.year = year
        self.semester = semester
        self.could_answer = could_answer
        self.have_answered = have_answered
        self.did_not_follow = did_not_follow
        self.performance_scale = performance_scale
        self.prereq_scale = prereq_scale

    def __key__(self):
        return (self.year, self.semester, self.could_answer, self.have_answered, self.did_not_follow, self.performance_scale, self.prereq_scale)

    def __repr__(self):
        templ = "Course evaluation from {}, {} semester: {} could answer, {} have answered, {} did not follow. Performance: {}, prerequisites: {}"
        return templ.format(self.year, self.semester, self.could_answer, self.have_answered, self.did_not_follow, self.performance_scale, self.prereq_scale)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        comparisons = [
            self.year == other.year,
            self.semester == other.semester,
            self.could_answer == other.could_answer,
            self.have_answered == other.have_answered,
            self.did_not_follow == other.did_not_follow,
            self.performance_scale == other.performance_scale,
            self.prereq_scale == other.prereq_scale
        ]
        for x, comp in enumerate(comparisons):
            if not comp:
                print "course run differs at {} ({} total)".format(x, len(comparisons))
        return reduce(operator.and_, comparisons)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key__())