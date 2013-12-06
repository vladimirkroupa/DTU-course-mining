import re
import operator
from abc import ABCMeta, abstractmethod

class Token(object):
    __metaclass__ = ABCMeta

    def is_course(self):
        return False

    def is_operator(self):
        return False

    def is_left_paren(self):
        return False

    def is_right_paren(self):
        return False

    @classmethod
    def from_string(self, token_str):
        map = {'(': LeftParenthesis(),
               ')': RightParenthesis(),
               '/': AnyOf(),
               '.': AllOf()}

        return map.get(token_str, Course(token_str))

class NAryOperator(Token):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def is_operator(self):
        return True

    @abstractmethod
    def precedence(self):
        pass

    def _compare(self, method, other):
        return isinstance(self, NAryOperator) and isinstance(other, NAryOperator) \
            and method(self.precedence(), other.precedence())

    def __lt__(self, other):
        return self._compare(operator.lt, other)

    def __le__(self, other):
        return self._compare(operator.le, other)

    def __eq__(self, other):
        return self._compare(operator.eq, other)

    def __ne__(self, other):
        return self._compare(operator.ne, other)

    def __gt__(self, other):
        return self._compare(operator.gt, other)

    def __ge__(self, other):
        return self._compare(operator.ge, other)


class AllOf(NAryOperator):

    def precedence(self):
        return 1

    def __repr__(self):
        return "."


class AnyOf(NAryOperator):

    def precedence(self):
        return 2

    def __repr__(self):
        return "/"


class Course(Token):

    def __init__(self, code):
        self.code = code

    def is_course(self):
        return True

    def __repr__(self):
        return self.code


class LeftParenthesis(Token):

    def is_left_paren(self):
        return True

    def __repr__(self):
        return "("


class RightParenthesis(Token):

    def is_right_paren(self):
        return True

    def __repr__(self):
        return ")"


class ShuntingYard(object):

    def __init__(self, input):
        self.operator_stack = []
        self.output_stack = []
        self.input = self._tokenize(input)

    def _tokenize(self, input):
        regex = re.compile(r'/|\.|\(|\)|[A-Za-z0-9]+')
        return [Token.from_string(token_str) for token_str in regex.findall(input)]

    def _operator_on_top(self):
        if len(self.operator_stack) and self.operator_stack[-1].is_operator():
            return self.operator_stack[-1]
        else:
            return None

    def _pop_onto_output(self):
        operator = self.operator_stack.pop()
        operands = 2
        for op in reversed(self.operator_stack):
            if op == operator:
                operands += 1
                self.operator_stack.pop()
            else:
                break
        for x in xrange(0, operands):
            operand = self.output_stack.pop()
            operator.add_child(operand)

        # operand = self.output_stack.pop()
        # operator.add_child(operand)
        self.output_stack.append(operator)

    def process(self):
        while len(self.input):
            token = self.input.pop(0)
            if token.is_course():
                self.output_stack.append(token)
            elif token.is_operator():
                # while there is an operator token o2 on the top of the stack and o1 has less precedence than o2
                while self._operator_on_top() and token < self._operator_on_top():
                    self._pop_onto_output()
                self.operator_stack.append(token)
            elif token.is_left_paren():
                self.operator_stack.append(token)
            elif token.is_right_paren():
                while not self.operator_stack[-1].is_left_paren():
                    self._pop_onto_output()
                self.operator_stack.pop()
            else:
                raise ValueError('Unmatched token: ' + token)

        while len(self.operator_stack) > 0:
            op = self.operator_stack.pop()
            if op.is_left_paren() or op.is_right_paren():
                raise ValueError('Mismatched parentheses.')
            self.operator_stack.append(op)
            self._pop_onto_output()

        return self.output_stack[0]