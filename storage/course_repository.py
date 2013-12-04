from model.course import Course
from model.department import Department
from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, Float, String
from sqlalchemy import create_engine, select

class CourseRepository(object):

    def __init__(self):
        self.db = create_engine('sqlite:///courses.db', echo=True)

        metadata = MetaData()

        self.departments = Table('departments', metadata,
                            Column('code', String, primary_key=True),
                            Column('name_en', String))

        self.courses = Table('courses', metadata,
                        Column('code', String, primary_key=True),
                        Column('language', String),
                        Column('title_en', String),
                        Column('title_da', String),
                        Column('evaluation_type', String),
                        Column('ects_credits', Float),
                        Column('course_type', String),
                        Column('prereqs', String),
                        Column('prereq_desc', String),
                        Column('department_code', String, ForeignKey('departments.code')))

        metadata.create_all(self.db)

    def __del__(self):
        self.db.dispose()

    def clear(self):
        del_c = self.courses.delete()
        del_d = self.departments.delete()
        self.db.execute(del_c)
        self.db.execute(del_d)

    def store_course_item(self, course):
        dep_code = course['department']['code']
        dep = self.find_department_by_code(dep_code)
        if not dep:
            self.store_department_item(course['department'])

        ins = self.courses.insert().values(
            code = course['code'],
            language = course['language'],
            title_en = course['title_en'],
            title_da = course['title_da'],
            evaluation_type = course['evaluation_type'],
            ects_credits = course['ects_credits'],
            course_type = course['course_type'],
            prereqs = course.get('prereqs', ''),
            prereq_desc = course.get('prereq_desc', ''),
            department_code = dep_code
        )

        self.db.execute(ins)

    def find_course_by_code(self, code):
        code = unicode(code)
        sel = select([self.courses, self.departments], use_labels=True)\
            .select_from(self.courses.join(self.departments))\
            .where(self.courses.c.code == code)
        result = self.db.execute(sel)
        courses = [self._map_course(row) for row in result]
        if len(courses) == 0:
            return None
        else:
            return courses[0]

    def store_department_item(self, department):
        ins = self.departments.insert().values(code=department['code'], name_en=department['title_en'])
        self.db.execute(ins)

    def find_department_by_code(self, code):
        code = unicode(code)
        sel = select([self.departments], use_labels=True).where(self.departments.c.code == code)
        result = self.db.execute(sel)
        departments = [self._map_department(row) for row in result]
        if len(departments) == 0:
            return None
        else:
            return departments[0]

    def _map_course(self, row_proxy):
        department = self._map_department(row_proxy)
        return Course(
            code = row_proxy['courses_code'],
            language = row_proxy['courses_language'],
            title_en = row_proxy['courses_title_en'],
            title_da = row_proxy['courses_title_da'],
            evaluation_type = row_proxy['courses_evaluation_type'],
            ects_credits = row_proxy['courses_ects_credits'],
            course_type = row_proxy['courses_course_type'],
            department = department
        )

    def _map_department(self, row_proxy):
        return Department(
            code = row_proxy['departments_code'],
            title_en = row_proxy['departments_name_en'],
            title_da = None
        )
