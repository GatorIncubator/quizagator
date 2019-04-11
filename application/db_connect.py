## PACKAGE IMPORTS

from application import app
import sqlite3 #imports database sqlite3
from flask import g, session, escape
from functools import wraps

DATABASE = 'database.db' # database

# Connecting to database sqlite3
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#close connection to DATABASE
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#query the DATABASE
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    returnval = cur.fetchall()
    cur.close()
    return (returnval[0] if returnval else None) if one else returnval

#insert a value into the DATABASE
def insert_db(query, args=()):
	"""
    Runs queries to insert into the database
	"""
	db = get_db()
	db.execute(query, args)
	db.commit()


##############
### STUDENT FUNCS
#######


def validate_student(func):
	"""
    Checks to make sure the login is a student, or returns route to teacher
	"""
	@wraps(func)
	def f(*args, **kwds):
		if not 'isTeacher' in session:
			return redirect("/")
		if session['isTeacher'] == 1:
			return redirect("/teachers/")
		return func(*args, **kwds)
	return f

def get_student_classes():
	class_data = query_db("SELECT classes.id, classes.name FROM classes JOIN roster ON roster.class_id = classes.id where people_id=?;", [session['id']])
	classes = []
	for class_info in class_data:
		student_class = {}
		student_class['id'] = class_info[0]
		student_class['name'] = class_info[1]
		classes.append(student_class)
	return classes


def get_student_grade(class_id):
	"""
	Gets all the grades given to the student.
	"""
	grades = []
	quiz_grade = query_db("SELECT quizzes.name, grade FROM quiz_grades JOIN quizzes ON quiz_grades.quiz_id=quizzes.id JOIN topics on quizzes.topic_id=topics.id JOIN classes ON topics.class_id=classes.id WHERE student_id=? AND topics.class_id=?;", [session['id'], class_id])
	for grade in quiz_grade:
		student_grade_quiz = {}
		student_grade_quiz['thing_name'] = grade[0]
		student_grade_quiz['grade'] = grade[1]
		grades.append(student_grade_quiz)
	assignment_grade = query_db("SELECT assignments.name, grade FROM assignment_grades JOIN assignments ON assignment_grades.assignment_id=assignments.id JOIN topics on assignments.topic_id=topics.id JOIN classes ON topics.class_id=classes.id WHERE student_id=? AND topics.class_id=?;", [session['id'], class_id])
	for grade in assignment_grade:
		student_grade_assignment = {}
		student_grade_assignment['thing_name'] = grade[0]
		student_grade_assignment['grade'] = grade[1]
		grades.append(student_grade_assignment)
	return grades

# def get_student_feedback(class_id):
# 	feedback = query_db("SELECT assignments.name, grade FROM assignment_grades JOIN assignments ON assignment_grades.assignment_id=assignments.id JOIN topics on assignments.topic_id=topics.id JOIN classes ON topics.class_id=classes.id WHERE student_id=? AND topics.class_id=?;", [session['id'], class_id])
# 	for grade in assignment_grade:
# 		student_grade_assignment = {}
# 		student_grade_assignment['thing_name'] = grade[0]
# 		student_grade_assignment['grade'] = grade[1]
# 		grades.append(student_grade_assignment)
# 	return grades

#################
###TEACHER FUNCS
##################


def validate_teacher(func):
	"""
	Checks to make sure the login is a teacher, or returns route to student
	"""
	@wraps(func)
	def f(*args, **kwds):
		if not 'isTeacher' in session:
			return redirect("/")
		if session['isTeacher'] == 0:
			return redirect("/students/")
		return func(*args, **kwds)
	return f


def get_teacher_class():
	"""
	Gets the classes from class_data that a teacher has
	"""
	class_data = query_db("select id, name from classes where teacher_id = ?;", [session['id']])
	classes = []
	for part in class_data:
		class_dict = {}
		class_dict['id'] = part[0]
		class_dict['name'] = str(part[1])
		classes.append(class_dict)
	return classes

def get_teacher_topic_all():
	"""
	Gets the topics that a teacher has
	"""
	topic_data = query_db("select topics.id, topics.name, classes.name from topics join classes on topics.class_id=classes.id where teacher_id=?;", [session['id']])
	topics = []
	for topic in topic_data:
		topic_dict_teacher = {}
		topic_dict_teacher['id'] = topic[0]
		topic_dict_teacher['name'] = escape(str(topic[1]))
		topic_dict_teacher['class'] = escape(str(topic[2]))
		topics.append(topic_dict_teacher)
	return topics

def get_class_topic(class_id):
	"""
	Gets all of the topics in a specific class.
	"""
	topic_data = query_db("select id, name from topics where class_id=?", [class_id])
	topics = []
	for topic in topic_data:
		topic_dict_class = {}
		topic_dict_class['id'] = topic[0]
		topic_dict_class['name'] = topic[1]
		topics.append(topic_dict_class)
	return topics

def get_teacher_assign():
	"""
	Gets all of the assignments in teacher class.
	"""
	assignment_data = query_db("select assignments.id, assignments.name, assignments.due_date from assignments join topics on assignments.topic_id=topics.id join classes on topics.class_id=classes.id where teacher_id=?;", [session['id']])
	assignments = []
	for assignment in assignment_data:
		assignment_dict_teach = {}
		assignment_dict_teach['id'] = assignment[0]
		assignment_dict_teach['name'] = assignment[1]
		assignment_dict_teach['due_date'] = assignment[2]
		assignments.append(assignment_dict_teach)
	return assignments

def get_class_assign(class_id):
	"""
	Obtains all of the assignments for a class.
	"""
	assignment_data = query_db("select id, name, due_date from assignments where topic_id=(select id from topics where class_id=?);", [class_id])
	assignments = []
	for assignment in assignment_data:
		assignment_dict_class = {}
		assignment_dict_class['id'] = assignment[0]
		assignment_dict_class['name'] = str(assignment[1])
		assignment_dict_class['due_date'] = assignment[2]
		assignments.append(assignment_dict_class)
	return assignments

def get_topic_assign(topic_id):
	"""
	Obtains assignments in a topic.
	"""
	assignment_data = query_db("select id, name, due_date from assignments where topic_id=?;", [topic_id])
	assignments = []
	for assignment in assignment_data:
		topic_assign_dict = {}
		topic_assign_dict['id'] = assignment[0]
		topic_assign_dict['name'] = str(assignment[1])
		topic_assign_dict['due_date'] = assignment[2]
		assignments.append(topic_assign_dict)
	return assignments

def get_quiz_teacher():
	"""
	Obtains quizzes created by the teacher.
	"""
	quiz_data = query_db("select id, name from quizzes where creator_id=?;", [session['id']])
	quizzes = []
	for quiz in quiz_data:
		quiz_dict = {}
		quiz_dict['id'] = quiz[0]
		quiz_dict['name'] = quiz[1]
		quizzes.append(quiz_dict)
	return quizzes

def get_topic_quiz(topic_id):
	"""
	Obtains quizzes in a particular topic.
	"""
	quiz_data = query_db("select id, name from quizzes where topic_id=?;", [topic_id])
	quizzes = []
	for quiz in quiz_data:
		quiz_topic = {}
		quiz_topic['id'] = quiz[0]
		quiz_topic['name'] = quiz[1]
		quizzes.append(quiz_topic)
	return quizzes

def get_class_quiz(class_id):
	"""
	Obtains quizzes in a particular class.
	"""
	quiz_data = query_db("SELECT quizzes.id, quizzes.name FROM quizzes JOIN topics ON topics.id=quizzes.topic_id WHERE topics.class_id=?;", [class_id])
	quizzes = []
	for quiz in quiz_data:
		quiz_class = {}
		quiz_class['id'] = quiz[0]
		quiz_class['name'] = quiz[1]
		quizzes.append(quiz_class)
	return quizzes

def get_students_class(class_id):
	"""
	Gets all of the students in a class.
	"""
	student_data = query_db("SELECT people.id, name FROM people JOIN roster ON roster.people_id=people.id WHERE roster.class_id=?;", [class_id])
	student_class = []
	for student in student_data:
		student_dict = {}
		student_dict['id'] = student[0]
		student_dict['name'] = student[1]
		student_class.append(student_dict)
	return student_class

def get_class_grades(class_id):
	"""
	Obtains grades given to students in a class.
	"""

	grades = []
	quiz_grades = query_db("SELECT people.name, quizzes.name, grade FROM quiz_grades JOIN people ON quiz_grades.student_id=people.id JOIN quizzes ON quiz_grades.quiz_id=quizzes.id JOIN topics ON quizzes.topic_id=topics.id JOIN classes ON topics.class_id=classes.id WHERE classes.id=?;", [class_id])
	for grade in quiz_grades:
		grade_class = {}
		grade_class['student_name'] = grade[0]
		grade_class['thing_name'] = str(grade[1]) + " (Quiz)"
		grade_class['grade'] = grade[2]
		grades.append(grade_class)
	assignment_grades = query_db("SELECT people.name, assignments.name, grade FROM assignment_grades JOIN people ON assignment_grades.student_id=people.id JOIN assignments ON assignment_grades.assignment_id=assignments.id JOIN topics ON assignments.topic_id=topics.id JOIN classes ON topics.class_id=classes.id WHERE classes.id=?;", [class_id])
	for grade in assignment_grades:
		grade_assign = {}
		grade_assign['student_name'] = grade[0]
		grade_assign['thing_name'] = str(grade[1]) + " (Assignment)"
		grade_assign['grade'] = grade[2]
		grades.append(grade_assign)
	return grades
