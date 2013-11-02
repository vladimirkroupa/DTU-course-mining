from collections import defaultdict

class PageCounter():

    def __init__(self, total_grade_pages, total_evaluation_pages, log = None):
        self.total_grade_pages = total_grade_pages
        self.total_evaluation_pages = total_evaluation_pages
        self.grade_pages_processed = defaultdict(int)
        self.evaluation_pages_processed = defaultdict(int)
        self.log = log

    def count_grade_page(self, course_code):
        self.grade_pages_processed[course_code] += 1
        if self.log:
            self.log("Scraped {} grade pages of {} total for course {}.".format(self.grade_pages_processed[course_code], self.total_grade_pages, course_code))

    def count_evaluation_page(self, course_code):
        self.evaluation_pages_processed[course_code] += 1
        if self.log:
            self.log("Scraped {} evaluation pages of {} total for course {}.".format(self.grade_pages_processed[course_code], self.total_evaluation_pages, course_code))

    def course_processed(self, course_code):
        all_grade_pages = self.grade_pages_processed[course_code] == self.total_grade_pages
        all_evaluation_pages = self.evaluation_pages_processed[course_code] == self.total_evaluation_pages
        return all_grade_pages and all_evaluation_pages