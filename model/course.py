import operator

class Course:
    
    def __init__(self, code, language, title_en, title_da, evaluation_type, ects_credits, course_type, course_runs = []):
        self.code = code
        self.language = language
        self.title_en = title_en
        self.title_da = title_da
        self.evaluation_type = evaluation_type
        self.ects_credits = ects_credits
        self.course_type = course_type
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

    def __eq__(self, other):
        comparisons = [
            self.code == other.code,
            self.language == other.language,
            self.title_en == other.title_en,
            self.title_da == other.title_da,
            self.evaluation_type == other.evaluation_type,
            self.ects_credits == other.ects_credits,
            self.course_type == other.course_type,
            self.course_runs == other.course_runs
        ]
        return reduce(operator.and_, comparisons)