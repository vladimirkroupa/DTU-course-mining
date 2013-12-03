class EvaluationTypeProcessor(object):

    def __call__(self, eval_types):
        return [self.process(eval_type) for eval_type in eval_types]

    def process(self, eval_type):
        tokens = eval_type.split(',')
        eval_type = tokens[0]
        return eval_type.strip()


class Strip(object):

    def __call__(self, values):
        return [value.strip() for value in values]


class StripAndEncode(object):

    def __init__(self, encoding):
        self.encoding = encoding

    def __call__(self, values):
        return [s.strip().encode(self.encoding) for s in values]


class ParseCommaFloat(object):

    def __call__(self, values):
        return [float(value.replace(',', '.')) for value in values]
