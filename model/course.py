import operator

class Course:
    
    def __init__(self, code, language, title_en, title_da, evaluation_type, ects_credits, course_type, department = None, course_runs = []):
        self.code = code
        self.language = language
        self.title_en = title_en
        self.title_da = title_da
        self.evaluation_type = evaluation_type
        self.ects_credits = ects_credits
        self.course_type = course_type
        self.department = department
        self.course_runs = course_runs

    def add_course_run(self, course_run):
        self.course_runs.append(course_run)

    def is_7_grade_eval(self):
        pass


    def list_of_years_run(self):
        return []

    def run_of_year(self, year):
        if year not in self.list_of_years_run():
            return None # exception?
        else:
            pass

    def __repr__(self):
        templ = "{0}: {2} ({3}), taught in {1}, evaluation: {4}, ects credits: {5}, course type: {6}, department: {8}, course runs: {7}"
        return templ.format(self.code, self.language, self.title_en, self.title_da, self.evaluation_type,
                            self.ects_credits, self.course_type, self.course_runs, self.department)


    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        comparisons = [
            self.code == other.code,
            self.language == other.language,
            self.title_en == other.title_en,
            self.title_da == other.title_da,
            self.evaluation_type == other.evaluation_type,
            self.ects_credits == other.ects_credits,
            self.course_type == other.course_type,
            self.course_runs == other.course_runs,
            self.department == other.department
        ]
        return reduce(operator.and_, comparisons)