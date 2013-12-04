import re
import operator

class Node(object):

    def __init__(self):
        self.left = None
        self.right = None

    def add_children(self, left, right):
        self.left = left
        self.right = right

class Course(Node):

    @classmethod
    def from_token(cls, token):
        return Course(token)

    def __init__(self, course_code):
        super(Course, self).__init__()
        self.value = course_code

    def __repr__(self):
        return self.value

class Operator(Node):

    @classmethod
    def from_token(cls, token):
        if token == '/':
            return OrOperator()
        if token == '.':
            return AndOperator()

    def _compare(self, method, other):
        return isinstance(self, Operator) and isinstance(other, Operator) and method(self.precedence(), other.precedence())

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

class AndOperator(Operator):

    def precedence(self):
        return 1

    def __repr__(self):
        return "."

class OrOperator(Operator):

    def precedence(self):
        return 2

    def __repr__(self):
        return "/"

def tokenize(input):
    regex = re.compile(r'/|\.|\(|\)|[A-Za-z0-9]+')
    return regex.findall(input)

def is_operator(token):
    return token in ['/', '.']

def is_left_paren(token):
    return token == '('

def is_right_paren(token):
    return token == ')'

def is_course_code(token):
    return token not in ['/', '.', '(', ')']

def pop_onto_output(operator_stack, output_stack):
    operator = operator_stack.pop()
    l_operand = output_stack.pop()
    r_operand = output_stack.pop()
    operator.add_children(l_operand, r_operand)
    output_stack.append(operator)

def shunting_yard(input):
    operator_stack = []
    output_stack = []

    for token in tokenize(input):
        if is_course_code(token):
            output_stack.append(Course.from_token(token))
        elif is_operator(token):
            o1 = Operator.from_token(token)
            # while there is an operator token o2 on the top of the stack and o1 has less precedence than o2
            while len(operator_stack) > 0 and isinstance(operator_stack[-1], Operator) and o1 < operator_stack[-1]:
                pop_onto_output(operator_stack, output_stack)
            operator_stack.append(o1)
        elif is_left_paren(token):
            operator_stack.append(token)
        elif is_right_paren(token):
            while not is_left_paren(operator_stack[-1]):
                pop_onto_output(operator_stack, output_stack)
            operator_stack.pop()
        else:
            raise ValueError('Unmatched token: ' + token)

    while len(operator_stack) > 0:
        op = operator_stack.pop()
        if is_left_paren(op) or is_right_paren(op):
            raise ValueError('Mismatched parentheses.')
        operator_stack.append(op)
        pop_onto_output(operator_stack, output_stack)

    return output_stack[0]