from pydot import Dot, Edge, Node
from shunting_yard import AllOf, AnyOf, Course
from shunting_yard import ShuntingYard

class PydotAstWalker(object):

    def __init__(self, ast_root, course_code):
        self.course_code = course_code
        self.ast = ast_root
        self.graph = Dot(graph_type='digraph')
        self.counter = 0

    def _unique_name(self, node):
        self.counter += 1
        return self.counter

    def genererate_graph(self):
        root_operator_node = self._visit_node(self.ast)
        course_root_node = Node(self.course_code)
        self.graph.add_node(course_root_node)
        self.graph.add_edge(Edge(course_root_node, root_operator_node))
        return self.graph

    def _visit_node(self, ast_node):
        if ast_node.is_course():
            node = Node(ast_node.code)
            self.graph.add_node(node)
            return node
        elif ast_node.is_operator():
            name = self._unique_name(ast_node)
            if isinstance(ast_node, AllOf):
                this_node = Node(name, label="AND", shape="square")
            else:
                this_node = Node(name, label="OR", shape="diamond")
            self.graph.add_node(this_node)
            child_nodes = [self._visit_node(child) for child in ast_node.children]
            for child in child_nodes:
                edge = Edge(this_node, child)
                self.graph.add_edge(edge)
            return this_node


def plot_prereqs(course):
    sy = ShuntingYard(course.prereq_string)
    root_operator = sy.process()
    walker = PydotAstWalker(root_operator, course.code)
    return walker.genererate_graph()


sy = ShuntingYard("27021/27025.27231/27025.27230.27430")
root_operator = sy.process()
walker = PydotAstWalker(root_operator, "27432")
graph = walker.genererate_graph()

graph.write('test2.png', format='png')
