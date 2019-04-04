from application import app
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import flash
from flask import escape
from functools import wraps
from .db_connect import *


## main teacher page
@app.route('/teachers/')
@validate_teacher
def teachers():

	## return the main page
	return render_template('/teachers/index.html', classes=get_teacher_class())

## classes home page
@app.route('/teachers/classes/')
@validate_teacher
def classes_page():
	return render_template('/teachers/classes.html', classes=get_teacher_class())

## create a class
@app.route('/teachers/classes/create/', methods=['GET', 'POST'])
@validate_teacher
def create_class():
	## request is GET
	if request.method == 'GET':
		return render_template('/teachers/classes/create.html')

	## request is post

	insert_db("insert into classes (teacher_id, name) values (?, ?);", [session['id'], request.form['name']])
	class_data = query_db("select id, name from classes order by id desc limit 1", one=True)
	flash("Your class, %s, was created with an id of %s." %(class_data[1], class_data[0]))
	return redirect("/teachers/classes/create/")

## class page for a class id
@app.route('/teachers/class/<class_id>/')
@validate_teacher
def class_page(class_id=None):
	class_name = query_db("select name from classes where id=?", [class_id])
	class_name = class_name[0][0]
	return render_template('/teachers/class_page.html', class_id=class_id, class_name=class_name, topics=get_class_topic(class_id), assignments=get_class_assign(class_id), students=get_students_class(class_id), grades=get_class_grades(class_id))

## the main topics page for a teacher
@app.route('/teachers/topics/')
@validate_teacher
def topics_page():
	return render_template('/teachers/topics.html', classes=get_teacher_class(), topics=get_teacher_topic_all())

## create a topic
@app.route('/teachers/topics/create/', methods=['POST'])
@validate_teacher
def create_topic():
	insert_db("insert into topics (name, class_id) values (?, ?);", [request.form['name'], request.form['class']])
	flash("Your class was created.")
	return render_template('/teachers/topics.html', classes=get_teacher_class())

## individual topic page
# @app.route('/teachers/topics/<topic_id>/')
# @validate_teacher
# def topic_page(topic_id=None):
# 	topic_data = query_db("select name from topics where id=?", [topic_id], one=True)
# 	return render_template('/teachers/topic_page.html', assignments=get_topic_assign(topic_id), topic_name=str(topic_data[0]), quizzes=get_topic_quiz(topic_id))

######################################

# @app.route('/teachers/objectives/')
# @validate_teacher
# def teacher_objectives_home():
# 	return render_template('/teachers/objectives.html', classes=get_teacher_assign())

@app.route('/teachers/objectives/<topic_id>/')
@validate_teacher
def topic_page(topic_id=None):
	topic_data = query_db("select name from topics where id=?", [topic_id], one=True)
	return render_template('/teachers/topic_page.html', assignments=get_topic_assign(topic_id), topic_name=str(topic_data[0]), quizzes=get_topic_quiz(topic_id))


@app.route('/teachers/feedback/')
@validate_teacher
def teacher_feedback_home():
	return render_template('/teachers/feedback.html', classes=get_teacher_assign())

#################################

## main assignments page
@app.route('/teachers/assignments/')
@validate_teacher
def assignments_page():
	return render_template('/teachers/assignments.html', topics=get_teacher_topic_all(), assignments=get_teacher_assign())

## create an assignment
@app.route('/teachers/assignments/create/', methods=['POST'])
@validate_teacher
def create_assignment():
	##date is posted as yyyy-mm-dd
	insert_db("insert into assignments (name, description, due_date, topic_id) values (?, ?, ?, ?);", [request.form['name'], request.form['description'], request.form['due_date'], request.form['topic']])
	flash("The assignment was created.")
	return redirect('/teachers/assignments/')

## individual assignment page
@app.route('/teachers/assignments/<assignment_id>/')
@validate_teacher
def assignment_page(assignment_id):
	assignment_info = query_db("SELECT name, due_date, description FROM assignments WHERE id=?;", [assignment_id])
	for bit in assignment_info:
		name = bit[0]
		due_date = bit[1]
		description = bit[2]
	return render_template('/teachers/assignment_page.html', name=name, due_date=due_date, description=description)

##main quizzes page
@app.route('/teachers/quizzes/')
@validate_teacher
def quizzes_page():
	return render_template('/teachers/quizzes.html', topics=get_teacher_topic_all(), quizzes=get_quiz_teacher())

## create quiz
@app.route('/teachers/quizzes/create/', methods=['POST'])
@validate_teacher
def create_quiz():
	insert_db("insert into quizzes (topic_id, creator_id, name) values(?, ?, ?);", [request.form['topic'],  session['id'], request.form['name']])
	flash("The quiz was created.")
	return redirect("/teachers/quizzes/")

## individual quiz page
@app.route('/teachers/quizzes/<quiz_id>/')
@validate_teacher
def quiz_page(quiz_id=None):
	questions_db = query_db("select question_text, correct_answer, a_answer_text, b_answer_text, c_answer_text, d_answer_text from questions where quiz_id=?;", [quiz_id])
	questions = []
	for question in questions_db:
		quest_choice = {}
		quest_choice['text'] = question[0]
		quest_choice['correct'] = ["A", "B", "C", "D"][question[1]]
		quest_choice['a'] = question[2]
		quest_choice['b'] = question[3]
		quest_choice['c'] = question[4]
		quest_choice['d'] = question[5]
		questions.append(quest_choice)

	quiz_name = query_db("SELECT name FROM quizzes WHERE id=?;", [quiz_id])

	return render_template('/teachers/quiz_page.html', quiz_id=quiz_id, questions=questions, quiz_name=str(quiz_name[0][0]))

##create quiz question
@app.route('/teachers/questions/create/<quiz_id>/', methods=['POST'])
@validate_teacher
def create_question(quiz_id=None):
	insert_db("INSERT INTO questions (correct_answer, question_text, a_answer_text, b_answer_text, c_answer_text, d_answer_text, quiz_id) VALUES (?, ?, ?, ?, ?, ?, ?);", [str(request.form['answer']), str(request.form['question']), str(request.form['a_answer']), str(request.form['b_answer']), str(request.form['c_answer']), str(request.form['d_answer']), str(quiz_id)])
	flash("The question was created.")
	return redirect("/teachers/quizzes/%s/" %(quiz_id))

## add a grade
@app.route('/teachers/grades/add/<class_id>/', methods=['POST'])
@validate_teacher
def create_grade(class_id):
	insert_db("INSERT INTO assignment_grades (student_id, assignment_id, grade) VALUES (?, ?, ?);", [request.form['student'], request.form['assignment'], request.form['grade']])
	flash("Grade submitted.")
	return redirect('/teachers/class/%s/'%(class_id))
