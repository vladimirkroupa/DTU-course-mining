import storage.course_repository

repo = storage.course_repository.CourseRepository('sqlite:///courses.db')

course = repo.find_course_by_code("27420")

graph = course.transitive_prereq_graph(repo, 0)

graph.write('27420.png', format='png')