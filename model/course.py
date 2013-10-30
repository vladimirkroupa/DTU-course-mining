# -*- coding: utf-8 -*-

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
        self.course_runs = {}
        self.add_course_runs(course_runs)

    def add_course_runs(self, course_runs):
        for run in course_runs:
            self.add_course_run(run)

    def add_course_run(self, course_run):
        key = (course_run.year, course_run.semester)
        self.course_runs[key] = course_run

    def list_of_years_run(self):
        return []

    def all_course_runs(self):
        return self.course_runs.values()

    def get_course_run(self, year, semester):
        """
            semester = E / F
        """
        key = (year, semester)
        return self.course_runs.get(key)

    def run_of_year(self, year):
        if year not in self.list_of_years_run():
            return None # exception?
        else:
            pass

    def __repr__(self):
        templ = u"{0}: {2} ({3}), taught in {1}, evaluation: {4}, ects credits: {5}, course type: {6}, department: {8}, {9} course runs: {7}"
        result = templ.format(self.code, self.language, self.title_en, self.title_da, self.evaluation_type,
                            self.ects_credits, self.course_type, self.course_runs, self.department, len(self.course_runs))
        return result.encode("utf-8")

    def __str__(self):
        course_str = u"""{0}: {1} ({2})
        {3}
        {4}
        {5} credits
        {6}
        {7}
        {8} course runs:
        """.format(self.code, self.title_en, self.title_da, self.language, self.evaluation_type, self.ects_credits,
                   self.course_type, self.department, len(self.course_runs))
        for run in self.course_runs.values():
            course_str += str(run) + "\n"
        return course_str

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

    def __ne__(self, other):
        return not self.__eq__(other)