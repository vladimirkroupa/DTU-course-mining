class Course:
    
    def __init__(self, code, language, title_en, title_da, eval_type, ects, course_type):
        self.code = code
        self.language = language
        self.title_en = title_en
        self.title_da = title_da
        self.evaluation_type = eval_type
        self.ects_credits = ects
        self.course_type = course_type

    def is_7_grade_eval(self):
        pass


    def list_of_years_run(self):
        return []

    def run_of_year(self, year):
        if year not in self.list_of_years_run():
            return None # exception?
        else:
            pass
