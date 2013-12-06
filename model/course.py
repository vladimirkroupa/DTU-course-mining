# -*- coding: utf-8 -*-

import operator
from viz.shunting_yard import ShuntingYard
from viz.pydot_generator import PydotAstWalker

class Course:
    
    def __init__(self, code, language, title_en, title_da, evaluation_type, ects_credits, course_type, prereq_str = None, prereq_text = None, department = None, course_runs = [], evaluations = []):
        self.code = code
        self.language = language
        self.title_en = title_en
        self.title_da = title_da
        self.evaluation_type = evaluation_type
        self.ects_credits = ects_credits
        self.course_type = course_type
        self.department = department
        self.prereq_str = prereq_str
        self.prereq_text = prereq_text
        self.course_runs = {}
        self.evaluations = {}
        self.add_course_runs(course_runs)
        self.add_evaluations(evaluations)

    def prereq_graph(self):
        sy = ShuntingYard(self.prereq_str)
        root_operator = sy.process()
        walker = PydotAstWalker(root_operator, self.code)
        return walker.generate_graph()

    def add_course_runs(self, course_runs):
        for run in course_runs:
            self.add_course_run(run)

    def add_course_run(self, course_run):
        key = (course_run.year, course_run.semester)
        self.course_runs[key] = course_run

    def add_evaluations(self, evaluations):
        for evaluation in evaluations:
            self.add_evaluation(evaluation)

    def add_evaluation(self, evaluation):
        key = (evaluation.year, evaluation.semester)
        self.evaluations[key] = evaluation

    def all_course_runs(self):
        return self.course_runs.values()

    def all_evaluations(self):
        return self.evaluations.values()

    def get_course_run(self, year, semester):
        """
            semester = E / F
        """
        key = (year, semester)
        return self.course_runs.get(key)

    def get_evaluation(self, year, semester):
        """
            semester = E / F
        """
        key = (year, semester)
        return self.evaluations.get(key)

    def list_years_run(self):
        """
        :return: set of all years when the course was run.
        """
        years = set()
        for year, semester in self.course_runs.keys():
            years.add(year)
        return years

    def __repr__(self):
        templ = u"{0}: {2} ({3}), taught in {1}, evaluation: {4}, ects credits: {5}, course type: {6}, department: {8}, {9} course runs: {7}, evaluations: {8}"
        result = templ.format(self.code, self.language, self.title_en, self.title_da, self.evaluation_type,
                            self.ects_credits, self.course_type, self.course_runs, self.department, len(self.course_runs), len(self.evaluations))
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
                   self.course_type, self.department, len(self.course_runs), len(self.evaluations))
        for run in self.course_runs.values():
            course_str += str(run) + "\n"
        course_str += "{} evaluations:\n".format(len(self.evaluations))
        for eval in self.evaluations.values():
            course_str += str(eval) + "\n"
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
            self.evaluations == other.evaluations,
            self.department == other.department
        ]
        return reduce(operator.and_, comparisons)

    def __ne__(self, other):
        return not self.__eq__(other)