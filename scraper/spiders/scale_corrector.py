class ScaleCorrector():

    MIXED_SCALES = "mixed scales mode"
    DISABLED = "disabled"

    def __init__(self, mode):
        self.passed = 0
        self.failed = 0
        self.mode = mode

    def offer_line(self, header, value):
        if not self._enabled():
            return False

        recognized = False

        if header == u'Passed':
            self.passed = int(value)
            recognized = True
        elif header == u'Not passed':
            self.failed = int(value)
            recognized = True

        return recognized

    def _enabled(self):
        return self.mode != ScaleCorrector.DISABLED

    def _total(self):
        return self.passed + self.failed

    def apply_corrections(self, course_run):
        if not self._enabled():
            return

        registered = int(course_run['students_registered'])
        registered -= self._total()
        course_run['students_registered'] = str(registered)

        attended = int(course_run['students_attended'])
        attended -= self._total()
        course_run['students_attended'] = str(attended)

        passed = int(course_run.get('students_passed', 0))
        if passed > 0:
            passed -= self.passed
            course_run['students_passed'] = str(passed)
