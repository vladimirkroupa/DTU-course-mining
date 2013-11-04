import operator

class Evaluation():

    def __init__(self, year, semester, could_answer, have_answered, did_not_follow, performance_vector, prereq_vector):
        self.year = year
        self.semester = semester
        self.could_answer = could_answer
        self.have_answered = have_answered
        self.did_not_follow = did_not_follow
        self.performance_vector = performance_vector
        self.prereq_vector = prereq_vector

    def __key__(self):
        return (self.year, self.semester, self.could_answer, self.have_answered, self.did_not_follow, self.performance_vector, self.prereq_vector)

    def __repr__(self):
        templ = "Course evaluation from {}, {} semester: {} could answer, {} have answered, {} did not follow. Performance: {}, prerequisites: {}"
        return templ.format(self.year, self.semester, self.could_answer, self.have_answered, self.did_not_follow, self.performance_vector, self.prereq_vector)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        comparisons = [
            self.year == other.year,
            self.semester == other.semester,
            self.could_answer == other.could_answer,
            self.have_answered == other.have_answered,
            self.did_not_follow == other.did_not_follow,
            self.performance_vector == other.performance_vector,
            self.prereq_vector == other.prereq_vector
        ]
        return reduce(operator.and_, comparisons)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key__())