import datetime

class Storage():


    def readCourseBase(self):
        """Retrieves latest course base.

        :return: list of Courses or None if storage is empty.
        """
        pass

    def lastUpdateDate(self):
        """
        :return: retrieval date of latest course base or None if storage is empty.
        """
        pass

    def storeCourseBase(self, course_json):
        """
        :param course_json: json string containing scraped course information
        """