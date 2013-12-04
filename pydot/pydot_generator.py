from pydot import Dot, Edge, Node
from shunting_yard import AndOperator, OrOperator, Course
from shunting_yard import shunting_yard

def name_node(ast_node):
    if isinstance(ast_node, Course):
        return ast_node.__repr__()
    if isinstance(ast_node, OrOperator):
        return ast_node.left.__repr__() + "OR" + ast_node.right.__repr__()
    if isinstance(ast_node, AndOperator):
        return ast_node.left.__repr__() + "AND" + ast_node.right.__repr__()

def create_pydot_node(ast_node):
    if isinstance(ast_node, Course):
        return Node(name_node(ast_node), label=ast_node.value)
    if isinstance(ast_node, OrOperator):
        return Node(name_node(ast_node), label="OR", shape="diamond")
    if isinstance(ast_node, AndOperator):
        return Node(name_node(ast_node), label="AND", shape="square")

def parse_tree(root):
    graph = Dot(graph_type='digraph')
    _parse_tree(root, graph)
    return graph

def _parse_tree(root, graph):
    this = create_pydot_node(root)
    graph.add_node(this)

    if root.left:
        left = create_pydot_node(root.left)
        graph.add_node(left)
        graph.add_edge(Edge(this, left))
        _parse_tree(root.left, graph)
    if root.right:
        right = create_pydot_node(root.right)
        graph.add_node(right)
        graph.add_edge(Edge(this, right))
        _parse_tree(root.right, graph)


def plot_prereqs(course):
    root = shunting_yard(course.prereq_string)
    graph = parse_tree(root)

    course_node = Node(course.code)
    graph.add_node(course_node)

    root_node = create_pydot_node(root)
    graph.add_edge(Edge(course_node, root_node))

    return graph
