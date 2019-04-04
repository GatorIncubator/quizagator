from application import app
from flask import render_template, session, redirect, request, flash, escape
from functools import wraps
from .db_connect import *

@app.route('/students/')
@validate_student
def student_home():
	return render_template('/students/index.html', classes=get_student_classes())

@app.route('/students/classes/')
@validate_student
def student_classes_home():
	return render_template('/students/classes.html', classes=get_student_classes())

@app.route('/students/classes/join/', methods=['POST'])
@validate_student
def student_class_join():
	"""If student joins a class"""
	insert_db("INSERT INTO roster (people_id, class_id) VALUES (?, ?);", [session['id'], request.form['id']])
	flash("You joined the class with an id of %s" %(request.form['id']))
	return redirect("/students/classes")

@app.route('/students/class/<class_id>/')
@validate_student
def student_class_page(class_id):
	"""shows classes"""
	class_name = query_db("SELECT name FROM classes WHERE id=?;", [class_id], one=True)
	return render_template('/students/class_page.html', class_name=str(class_name[0]), topics=get_class_topic(class_id), assignments=get_class_assign(class_id), quizzes=get_class_quiz(class_id), grades=get_student_grade(class_id))

###############


@app.route('/students/objectives/')
@validate_student
def student_objectives_home():
	return render_template('/students/objectives.html', classes=get_student_classes())

@app.route('/students/feedback/')
@validate_student
def student_feedback_home():
	return render_template('/students/feedback.html', classes=get_student_classes())

#################

@app.route('/students/topics/<topic_id>/')
@validate_student
def student_topic_page(topic_id):
	topic_name = query_db("SELECT name FROM topics WHERE id=?;", [topic_id], one=True)
	return render_template('/students/topic_page.html', topic_name=str(topic_name[0]), assignments=get_topic_assign(topic_id), quizzes=get_topic_quiz(topic_id))

@app.route('/students/quizzes/<quiz_id>/')
@validate_student
def student_quiz_page(quiz_id):
	"""Allows students to view/take quizzes"""
	quiz_name = query_db("SELECT name FROM quizzes WHERE id=?;", [quiz_id])
	result = query_db("SELECT grade from quiz_grades WHERE quiz_id=? AND student_id=?;", [quiz_id, session['id']], one=True) #check if the person has already taken the test
	if result == None:
		questions_db = query_db("SELECT id, question_text, a_answer_text, b_answer_text, c_answer_text, d_answer_text FROM questions WHERE quiz_id=?;", [quiz_id])
		questions = []
		for question in questions_db:
			question_dict = {}
			question_dict['id'] = question[0]
			question_dict['text'] = question[1]
			question_dict['answers'] = [str(question[2]), str(question[3]), str(question[4]), str(question[5])]
			questions.append(question_dict)
		return render_template('/students/quiz_page.html', questions = questions,quiz_name=quiz_name[0][0], quiz_id=quiz_id)
	else:
		flash("You receieved a grade of {0}% on this quiz.".format(result[0]))
		return render_template('/students/quiz_page.html', quiz_name=quiz_name[0][0])

@app.route('/students/quizzes/grade/<quiz_id>/', methods=['POST'])
@validate_student
def grade_quiz(quiz_id):
	"""Grades the quizzes based on teacher input"""
	correct = 0.0
	questions = 0.0
	data = request.form
	question_ids  = [int(i) for i in data]
	answers = []
	for i in data:
		answers.append(eval("int(data['%s'])"%(i)))

	for i in range(len(answers)):
		correctAnswer = query_db("SELECT correct_answer FROM questions WHERE id=?;", [question_ids[i]], one=True)
		if int(correctAnswer[0]) == answers[i]:
			correct += 1.0
		questions += 1.0
	percent = (correct/questions)*100
	insert_db("INSERT INTO quiz_grades (student_id, quiz_id, grade) VALUES (?, ?, ?);", [session['id'], quiz_id, percent])
	return redirect("/students/quizzes/%s/"%(quiz_id))

@app.route('/students/assignments/<assignment_id>/')
@validate_student
def student_assignment_page(assignment_id):
	assignment_data = query_db("SELECT name, description, due_date FROM assignments WHERE id=?;", [assignment_id], one=True)
	name = assignment_data[0]
	description = assignment_data[1]
	due_date = assignment_data[2]
	return render_template('/students/assignment_page.html', name=name, description=description, due_date=due_date)
