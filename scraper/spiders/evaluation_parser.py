from scrapy.selector import HtmlXPathSelector
from util.scrapy_utils import *
from scraper.items import EvaluationItem
import re

class EvaluationParser():

    def __init__(self, log):
        self.log = log

    def parse_evaluation_page(self, response):
        course = response.request.meta['course']
        hxs = HtmlXPathSelector(response)

        stats_table = select_single(hxs, '//table[contains(tr/td/text(), "Statistics")]')
        answers_table = select_single(hxs, '//form/table[2]')
        heading_str = select_single(hxs, '//form/h2/text()').extract().encode('utf-8')

        evaluation = EvaluationItem()
        self.parse_year_semester(heading_str, evaluation)
        self.parse_stats_table(stats_table, evaluation)
        self.parse_answers_table(answers_table, evaluation)

        course['evaluations'].append(evaluation)

        course_code = course['code']
        page_counter = response.request.meta['counter']
        page_counter.count_evaluation_page(course_code)
        if page_counter.course_processed(course_code):
            return course

    def parse_year_semester(self, heading_str, evaluation):

        def parse_semester(sem_part):
            if sem_part == u'E':
                return u'Winter'
            elif sem_part == u'F':
                return u'Summer'
            elif sem_part == u'Jan':
                return u'January'
            else:
                raise Exception(u'Unknown semester code {}'.format(sem_part))

        def parse_year(year_part):
            return u"20" + year_part

        regex = re.compile("""(E|F|Jan)(?: )?(\d\d)""")
        r = regex.search(heading_str)
        groups = r.groups()
        check_len(groups, 2)
        semester_part, year_part = groups

        evaluation['year']= parse_year(year_part)
        evaluation['semester'] = parse_semester(semester_part)

    def parse_stats_table(self, stats_table, evaluation):
        xpath = 'tr[contains(td/text(), "{}")]/td[1]/b/text()'
        evaluation['could_answer'] = select_single(stats_table, xpath.format("could answer this evaluation form")).extract()
        evaluation['have_answered'] = select_single(stats_table, xpath.format("have answered this evaluation form")).extract()
        did_not_follow = stats_table.select(xpath.format("did not follow the course")).extract()
        if len(did_not_follow) == 1:
            evaluation['did_not_follow'] = did_not_follow[0]
        else:
            evaluation['did_not_follow'] = u'0'

    def parse_answers_table(self, table, evaluation):

        xpath_templ = 'tr[contains(td/em/text(), "{}")]'
        nth_xpath = '(following-sibling::tr[count(child::td) = 4]/td[3]/text())[{}]'

        def parse_question(table, question_text):
            xpath = xpath_templ.format(question_text)
            question_row = select_single(table, xpath)
            answer_1 = select_single(question_row, nth_xpath.format(1)).extract()
            answer_2 = select_single(question_row, nth_xpath.format(2)).extract()
            answer_3  = select_single(question_row, nth_xpath.format(3)).extract()
            answer_4 = select_single(question_row, nth_xpath.format(4)).extract()
            answer_5 = select_single(question_row, nth_xpath.format(5)).extract()
            return (answer_1, answer_2, answer_3, answer_4, answer_5)

        def parse_workload_question(table):
            return parse_question(table, 'I think my performance during the course is')

        def parse_prereq_question(table):
            return parse_question(table, 'I think the course description')

        workload_answers = parse_workload_question(table)
        prereq_answers = parse_prereq_question(table)

        evaluation['performance_much_less'] = workload_answers[0]
        evaluation['performance_less'] = workload_answers[1]
        evaluation['performance_same'] = workload_answers[2]
        evaluation['performance_more'] = workload_answers[3]
        evaluation['performance_much_more'] = workload_answers[4]

        evaluation['prereq_too_low'] = prereq_answers[0]
        evaluation['prereq_low'] = prereq_answers[1]
        evaluation['prereq_adequate'] = prereq_answers[2]
        evaluation['prereq_high'] = prereq_answers[3]
        evaluation['prereq_too_high'] = prereq_answers[4]
