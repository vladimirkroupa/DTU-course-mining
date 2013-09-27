class Course:
    
    def __init__(self, course_item):
        self.code = course_item['code']
        self.language = course_item['language']
        self.title_en = course_item['title_en']
        self.title_da = course_item['title_da']
        self.evaluation_type = course_item['evaluation_type']
        self.ects_credits = course_item['ects_credits']
        self.course_type = course_item['course_type']

    def is_7_grade_eval(self):
        pass


    def list_of_years_run(self):
        return []

    def run_of_year(self, year):
        if year not in self.list_of_years_run():
            return None # exception?
        else:
            pass
