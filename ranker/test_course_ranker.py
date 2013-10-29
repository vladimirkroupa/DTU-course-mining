import unittest
from model.course import Course
from model.department import Department
from course_ranker import CourseRanker
from storage.storage import Storage
from mock import Mock

class CourseRankerTest(unittest.TestCase):

    BIO_DEP = Department(code = 27, title_en = 'Department of Systems Biology', title_da = 'Institut for Systembiologi')
    PHYS_DEP = Department(code = 10, title_en = 'Department of Physics', title_da = 'Institut for Fysik')

    COURSE_1 = Course(
            code = '27002',
            language = 'Danish',
            title_en = 'Life Science',
            title_da = 'Biovidenskab',
            evaluation_type = '7 step scale',
            ects_credits = 5,
            course_type = 'BSc',
            department = BIO_DEP,
    )
    COURSE_2 = Course(
            code = '27003',
            language = 'English',
            title_en = 'Life Science II',
            title_da = 'Biovidenskab II',
            evaluation_type = '7 step scale',
            ects_credits = 6,
            course_type = 'MSc',
            department = BIO_DEP,
    )
    COURSE_3 = Course(
            code = '28000',
            language = 'English',
            title_en = 'Nuclear reactors',
            title_da = 'Atomreaktorer',
            evaluation_type = '7 step scale',
            ects_credits = 7,
            course_type = 'MSc',
            department = PHYS_DEP,
    )

    ALL_COURSES = [COURSE_1, COURSE_2, COURSE_3]

    storageStub = Storage()
    storageStub.list_all_courses = Mock(return_value = ALL_COURSES)
    test_object = CourseRanker(storageStub)

    def test_all_courses(self):
        expected_courses = self.ALL_COURSES
        courses = self.test_object.course_ranking()
        self.assertEquals(expected_courses, courses)

    def test_department_bio(self):
        expected_courses = [self.COURSE_1, self.COURSE_2]
        courses = self.test_object.course_ranking(department = self.BIO_DEP)
        self.assertEquals(expected_courses, courses)

    def test_department_phys(self):
        expected_courses = [self.COURSE_3]
        courses = self.test_object.course_ranking(department = self.PHYS_DEP)
        self.assertEquals(expected_courses, courses)

    def test_course_type_bsc(self):
        expected_courses = [self.COURSE_1]
        courses = self.test_object.course_ranking(course_type = 'BSc')
        self.assertEquals(expected_courses, courses)

    def test_course_type_msc(self):
        expected_courses = [self.COURSE_2, self.COURSE_3]
        courses = self.test_object.course_ranking(course_type = 'MSc')
        self.assertEquals(expected_courses, courses)

    def test_course_type_department(self):
        courses_bio_bsc = self.test_object.course_ranking(department = self.BIO_DEP, course_type = 'BSc')
        courses_bio_msc = self.test_object.course_ranking(department = self.BIO_DEP, course_type = 'MSc')
        courses_phys_bsc = self.test_object.course_ranking(department = self.PHYS_DEP, course_type = 'BSc')
        courses_phys_msc = self.test_object.course_ranking(department = self.PHYS_DEP, course_type = 'MSc')
        self.assertEquals([self.COURSE_1], courses_bio_bsc)
        self.assertEquals([self.COURSE_2], courses_bio_msc)
        self.assertEquals([], courses_phys_bsc)
        self.assertEquals([self.COURSE_3], courses_phys_msc)


if __name__ == '__main__':
    unittest.main()