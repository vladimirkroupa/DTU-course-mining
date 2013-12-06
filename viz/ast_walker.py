from pydot import Dot, Edge, Node
from shunting_yard import AllOf

class PydotAstWalker(object):

    def __init__(self, ast_root, course_code, valid_expr=True):
        self.course_code = course_code
        self.valid_expr = valid_expr
        self.ast = ast_root
        self.graph = Dot(graph_type='digraph')

    def _name_node(self, node):
        if node.is_course():
            # what if not leaf node?
            return node.code
        elif node.is_operator():
            name = str(node)
            for child in node.children:
                name += self._name_node(child)
            return name

    def generate_graph(self):
        course_root_node = Node(self.course_code)
        if not self.ast:
            if not self.valid_expr:
                return  Node(self.course_code, fillcolor='red')
            else:
                return course_root_node
        root_operator_node = self._visit_node(self.ast)
        self.graph.add_node(course_root_node)
        self.graph.add_edge(Edge(course_root_node, root_operator_node))
        return self.graph

    def _visit_node(self, ast_node):
        if ast_node.is_course():
            node = Node(ast_node.code)
            self.graph.add_node(node)
            if not ast_node.is_leaf():
                child = self._visit_node(ast_node.child)
                edge = Edge(node, child)
                self.graph.add_edge(edge)
            return node
        elif ast_node.is_operator():
            name = self._name_node(ast_node)
            if isinstance(ast_node, AllOf):
                this_node = Node(name, label=str(ast_node), shape="square")
            else:
                this_node = Node(name, label=str(ast_node), shape="diamond")
            self.graph.add_node(this_node)
            child_nodes = [self._visit_node(child) for child in ast_node.children]
            for child in child_nodes:
                edge = Edge(this_node, child)
                self.graph.add_edge(edge)
            return this_node