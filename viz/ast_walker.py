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
        course_root_node = Node(self.course_code, style="filled", colorscheme="set35", fillcolor="5")
        if not self.ast:
            if not self.valid_expr:
                return Node(self.course_code, style="filled", colorscheme="set35", fillcolor="4")
            else:
                return course_root_node
        edges = set()
        root_operator_node = self._visit_node(self.ast, edges)
        for edge in edges:
            self.graph.add_edge(edge.to_pydot_edge())
        self.graph.add_node(course_root_node)
        self.graph.add_edge(Edge(course_root_node, root_operator_node))
        return self.graph

    def _visit_node(self, ast_node, edges):
        if ast_node.is_course():
            node = Node(ast_node.code, style="filled", colorscheme="set35", fillcolor="2")
            self.graph.add_node(node)
            if not ast_node.is_leaf():
                child = self._visit_node(ast_node.child, edges)
                edge = UniqueEdge(node, child)
                edges.add(edge)
            return node
        elif ast_node.is_operator():
            name = self._name_node(ast_node)
            if isinstance(ast_node, AllOf):
                this_node = Node(name, label=str(ast_node), shape="square", style="filled", colorscheme="set35", fillcolor="3")
            else:
                this_node = Node(name, label=str(ast_node), shape="diamond", style="filled", colorscheme="set35", fillcolor="1")
            self.graph.add_node(this_node)
            child_nodes = [self._visit_node(child, edges) for child in ast_node.children]
            for child in child_nodes:
                edge = UniqueEdge(this_node, child)
                edges.add(edge)
            return this_node


class UniqueEdge(object):

    def to_pydot_edge(self):
        return Edge(self.src_node, self.dest_node)

    def __init__(self, src_node, dest_node):
        self.src_node = src_node
        self.dest_node = dest_node

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __key(self):
        return (self.src_node.to_string(), self.dest_node.to_string())

    def __hash__(self):
        return hash(self.__key())
