def map_leaves(root, function, recur_allowed):
        if root.is_course():
            function(root, recur_allowed)
        else:
            for child in root.children:
                map_leaves(child, function, recur_allowed)

class GraphAggregator(object):

    def __init__(self, course_repository):
        self.course_repo = course_repository

    def append_leaf_prereqs(self, prereq_ast, max_depth):
        map_leaves(prereq_ast, self._prereq_from_leaf, max_depth)
        return prereq_ast

    def _prereq_from_leaf(self, course_node, recur_allowed):
        if recur_allowed == 0:
            return
        course = self.course_repo.find_course_by_code(course_node.code)
        if course:
            print 'processing', course.code, ': ', course.prereq_expr
            root = course._prereq_ast()
            if root is not None:
                course_node.set_child(root)
                map_leaves(root, self._prereq_from_leaf, recur_allowed - 1)