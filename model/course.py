# -*- coding: utf-8 -*-

import operator
from viz.shunting_yard import ShuntingYard
from viz.ast_walker import PydotAstWalker
from viz.graph_aggregator import GraphAggregator

class Course:
    
    def __init__(self, code, language, title_en, title_da, evaluation_type, ects_credits, course_type, prereq_expr = None, prereq_desc = None, department = None, course_runs = [], evaluations = []):
        self.code = code
        self.language = language
        self.title_en = title_en
        self.title_da = title_da
        self.evaluation_type = evaluation_type
        self.ects_credits = ects_credits
        self.course_type = course_type
        self.department = department
        self.prereq_expr = prereq_expr
        self.prereq_desc = prereq_desc
        self.course_runs = {}
        self.evaluations = {}
        self.add_course_runs(course_runs)
        self.add_evaluations(evaluations)

    def _validate_prereq_expr(self):
        return True

    def _fix_prereq_expr(self):
        def ad_hoc_unmatched_operator_fix(expr):
            return expr.replace(".)", ")")

        def remove_spaces(expr):
            return expr.replace(' ', '')

        def remove_front_end_operator(expr):
            if expr[0] in ('.', '/'):
                expr = expr[1:]
            if expr[-1] in ('.', '/'):
                expr = expr[:-1]
            return expr

        return ad_hoc_unmatched_operator_fix(remove_front_end_operator(remove_spaces(self.prereq_expr)))

    def _prereq_ast(self):
        if self.prereq_expr is None or not self._validate_prereq_expr():
            return None
        expr = self._fix_prereq_expr()
        sy = ShuntingYard(expr)
        return sy.parse_ast()

    def transitive_prereq_graph(self, course_repository, max_depth = 10):
        aggregator = GraphAggregator(course_repository)

        root_operator = self._prereq_ast()
        aggregator.append_leaf_prereqs(root_operator, max_depth)
        walker = PydotAstWalker(root_operator, self.code, self._validate_prereq_expr())
        return walker.generate_graph()

    def prereq_graph(self):
        root_operator = self._prereq_ast()
        walker = PydotAstWalker(root_operator, self.code, self._validate_prereq_expr())
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