from storage.course_repository import CourseRepository
from viz.shunting_yard import ShuntingYard
from viz.ast_walker import PydotAstWalker

def map_leaves(root, function, recur_allowed):
    if root.is_course():
        function(root, recur_allowed)
    else:
        for child in root.children:
            map_leaves(child, function, recur_allowed)

def foo(course_node, recur_allowed):
    if recur_allowed == 0:
        return
    course = repo.find_course_by_code(course_node.code)
    if course:
        print course.code, course.prereq_expr
        root = course._prereq_ast()
        if root is not None:
            course_node.set_child(root)
            map_leaves(root, foo, recur_allowed - 1)

repo = CourseRepository()
course = repo.find_course_by_code("27420")

root_operator = course._prereq_ast()
map_leaves(root_operator, foo, 0)

walker = PydotAstWalker(root_operator, "27254")

graph = walker.generate_graph()
graph.write('/tmp/test.png', format='png')








