from model.course import Course
from model.department import Department
from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, Float, String
from sqlalchemy import create_engine, select

class CourseRepository(object):

    def __init__(self):
        self.db = create_engine('sqlite:///:memory:', echo=True)

        metadata = MetaData()

        self.departments = Table('departments', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('code', String),
                            Column('name_en', String))

        self.courses = Table('courses', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('code', String),
                        Column('language', String),
                        Column('title_en', String),
                        Column('title_da', String),
                        Column('evaluation_type', String),
                        Column('ects_credits', Float),
                        Column('course_type', String),
                        Column('department_id', Integer, ForeignKey('departments.id')))

        metadata.create_all(self.db)

    def __del__(self):
        self.db.dispose()

    def store_course(self, course):
        dep_id = self.find_department_by_code(course.department.code)
        if not dep_id:
            dep_id = self.store_department(course.department)

        ins = self.courses.insert().values(
            code = course.code,
            language = course.language,
            title_en = course.title_en,
            title_da = course.title_da,
            evaluation_type = course.evaluation_type,
            ects_credits = course.ects_credits,
            course_type = course.course_type,
            department_id = dep_id
        )

        res = self.db.execute(ins)
        return res.inserted_primary_key[0]

    def find_course_by_code(self, code):
        code = unicode(code)
        sel = select([self.courses, self.departments]).where(self.courses.c.code == code)
        result = self.db.execute(sel)
        courses = [self._map_course(row) for row in result]
        if len(courses) == 0:
            return None
        else:
            return courses[0]

    def store_department(self, department):
        ins = self.departments.insert().values(code=department.code, name_en=department.name_en)
        res = self.db.execute(ins)
        return res.inserted_primary_key[0]

    def find_department_by_code(self, code):
        code = unicode(code)
        sel = select([self.departments]).where(self.departments.c.code == code)
        result = self.db.execute(sel)
        departments = [self._map_department(row) for row in result]
        if len(departments) == 0:
            return None
        else:
            return departments[0]

    def _map_course(self, row_proxy):
        department = self._map_department(row_proxy)
        return Course(
            code = row_proxy['code'],
            language = row_proxy['language'],
            title_en = row_proxy['title_en'],
            title_da = row_proxy['title_da'],
            evaluation_type = row_proxy['evaluation_type'],
            ects_credits = row_proxy['ects_credits'],
            course_type = row_proxy['course_type'],
            department = department
        )

    def _map_department(self, row_proxy):
        return Department(
            code = row_proxy['code'],
            title_en = row_proxy['name_en'],
            title_da = None
        )
