""" teacher endpoints """

import flask

from application import app
from . import db_connect as db


@app.route("/teachers/")
@db.validate_teacher
def teachers():
    """ main teacher page """
    return flask.render_template("/teachers/index.html", classes=db.get_teacher_class())


@app.route("/teachers/classes/")
@db.validate_teacher
def classes_page():
    """ teacher's class list """
    return flask.render_template(
        "/teachers/classes.html", classes=db.get_teacher_class()
    )


@app.route("/teachers/classes/create/", methods=["GET", "POST"])
@db.validate_teacher
def create_class():
    """ create a class """
    # flask.request is GET
    if flask.request.method == "GET":
        return flask.render_template("/teachers/classes/create.html")

    # flask.request is post
    db.insert_db(
        "INSERT INTO classes (teacher_id, name) VALUES (?, ?);",
        [flask.session["id"], flask.request.form["name"]],
    )
    class_data = db.query_db(
        "SELECT id, name FROM classes order by id desc limit 1", one=True
    )
    flask.flash(
        "Your class, %s, was created with an id of %s." % (class_data[1], class_data[0])
    )
    return flask.redirect("/teachers/classes/create/")


@app.route("/teachers/class/<class_id>/")
@db.validate_teacher
def class_page(class_id=None):
    """ specific class page """
    class_name = db.query_db("SELECT name FROM classes WHERE id=?", [class_id])
    class_name = class_name[0][0]
    return flask.render_template(
        "/teachers/class_page.html",
        class_id=class_id,
        class_name=class_name,
        topics=db.get_class_topic(class_id),
        assignments=db.get_class_assign(class_id),
        students=db.get_students_class(class_id),
        grades=db.get_class_grades(class_id),
    )


@app.route("/teachers/topics/")
@db.validate_teacher
def topics_page():
    """ the main topics page for teachers """
    return flask.render_template(
        "/teachers/topics.html",
        classes=db.get_teacher_class(),
        topics=db.get_teacher_topic_all(),
    )


@app.route("/teachers/topics/create/", methods=["POST"])
@db.validate_teacher
def create_topic():
    """ create a topic """
    db.insert_db(
        "INSERT INTO topics (name, class_id) VALUES (?, ?);",
        [flask.request.form["name"], flask.request.form["class"]],
    )
    flask.flash("Your class was created.")
    return flask.render_template(
        "/teachers/topics.html", classes=db.get_teacher_class()
    )


@app.route("/teachers/objectives/<topic_id>/")
@db.validate_teacher
def topic_page(topic_id=None):
    """ specific topic page """
    topic_data = db.query_db("SELECT name FROM topics WHERE id=?", [topic_id], one=True)
    return flask.render_template(
        "/teachers/topic_page.html",
        assignments=db.get_topic_assign(topic_id),
        topic_name=str(topic_data[0]),
        quizzes=db.get_topic_quiz(topic_id),
    )


@app.route("/teachers/feedback/")
@db.validate_teacher
def teacher_feedback_home():
    """ teacher feedback """
    return flask.render_template(
        "/teachers/feedback.html", classes=db.get_teacher_assign()
    )


@app.route("/teachers/assignments/")
@db.validate_teacher
def assignments_page():
    """ main assignments page """
    return flask.render_template(
        "/teachers/assignments.html",
        topics=db.get_teacher_topic_all(),
        assignments=db.get_teacher_assign(),
    )


@app.route("/teachers/assignments/create/", methods=["POST"])
@db.validate_teacher
def create_assignment():
    """ create an assignment -- date is posted as yyyy-mm-dd """
    db.insert_db(
        "INSERT INTO assignments (name, description, due_date, topic_id) "
        "VALUES (?, ?, ?, ?);",
        [
            flask.request.form["name"],
            flask.request.form["description"],
            flask.request.form["due_date"],
            flask.request.form["topic"],
        ],
    )
    flask.flash("The assignment was created.")
    return flask.redirect("/teachers/assignments/")


@app.route("/teachers/assignments/<assignment_id>/")
@db.validate_teacher
def assignment_page(assignment_id):
    """ individual assignment page """
    assignment_info = db.query_db(
        "SELECT name, due_date, description FROM assignments WHERE id=?;",
        [assignment_id],
    )
    for bit in assignment_info:
        name = bit[0]
        due_date = bit[1]
        description = bit[2]
    return flask.render_template(
        "/teachers/assignment_page.html",
        name=name,
        due_date=due_date,
        description=description,
    )


@app.route("/teachers/quizzes/")
@db.validate_teacher
def quizzes_page():
    """ main teacher quiz list page """
    return flask.render_template(
        "/teachers/quizzes.html",
        topics=db.get_teacher_topic_all(),
        quizzes=db.get_quiz_teacher(),
    )

#######################################
# DELETE
@db.validate_teacher
def quiz_page(quiz_id=None):
    """ individual quiz page """
    questions_db = db.query_db(
        "SELECT question_text, correct_answer, a_answer_text, b_answer_text, "
        "c_answer_text, d_answer_text FROM questions WHERE quiz_id=?;",
        [quiz_id],
    )
    questions = []
    for question in questions_db:
        quest_choice = {}
        quest_choice["text"] = question[0]
        quest_choice["correct"] = ["A", "B", "C", "D"][question[1]]
        quest_choice["a"] = question[2]
        quest_choice["b"] = question[3]
        quest_choice["c"] = question[4]
        quest_choice["d"] = question[5]
        questions.append(quest_choice)
########################################


@app.route("/teachers/quizzes/set/", methods=["POST"])
@db.validate_teacher
def set_quiz():
    """ creates a quiz using csv data """
    question = query_db(
        "SELECT questions.id, questions.type")
    # creates each question, one at a time
    item = []
    while question[0][0] is not None:

    # call respective method based on question type integer

##################################################
###                 OPEN ENDED                 ###
##################################################

        if question[0][1] = 0:
            question_oe = query_db(
            "SELECT question_text, FROM questions WHERE quiz_id=?",
            [quiz_id]
            )
            item.append[]

            # return flask.redirect("/teachers/questions/create/<quiz_id>/oe/")


##################################################
###             MULTIPLE CHOICES               ###
##################################################

        elif question[0][1] = 1:
            questions_db = db.query_db(
                "SELECT question_text, correct_answer, a_answer_text, b_answer_text, "
                "c_answer_text, d_answer_text FROM questions WHERE quiz_id=?;",
                [quiz_id],
            )
                quest_choice = {}
                quest_choice["text"] = question[0]
                quest_choice["correct"] = ["A", "B", "C", "D"][question[1]]
                quest_choice["a"] = question[2]
                quest_choice["b"] = question[3]
                quest_choice["c"] = question[4]
                quest_choice["d"] = question[5]
                item.append(quest_choice)

#################################################
###              RENDER TEMPLATE              ###
#################################################
        return flask.render_template(
            "/teachers/quiz_page.html",
            items=items,
            quiz_name=quiz_name[0][0],
            quiz_id=quiz_id,


        else:
            flask.flash("There was an error with a question type. Please check the file for mistakes.")
            return flask.redirect("/teachers/quizzes/")
    return flask.redirect("/teachers/quizzes/")


@app.route("/teachers/questions/create/<quiz_id>/oe/", methods=["POST"])
@db.validate_teacher
def create_oe_question(quiz_id=None):
    """ create open ended quiz question """
    db.insert_db(
    "INSERT INTO questions (student_response, question_text, quiz_id) "
    "VALUES (?, ?, ?);",
    [
    str(flask.request.form["answer"]), #create empty text value to be filled
    str(flask.request.form["question"]),
    str(quiz_id),
    ],
    )
    return flask.redirect("/teachers/quizzes/set/%s/" % (quiz_id))


@app.route("/teachers/questions/create/<quiz_id>/mc/", methods=["POST"])
@db.validate_teacher
def create_mc_question(quiz_id=None):
    """ create multiple choice quiz question """
    db.insert_db(
        "INSERT INTO questions (correct_answer, question_text, a_answer_text, "
        "b_answer_text, c_answer_text, d_answer_text, quiz_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);",
        [
            str(flask.request.form["answer"]),
            str(flask.request.form["question"]),
            str(flask.request.form["a_answer"]),
            str(flask.request.form["b_answer"]),
            str(flask.request.form["c_answer"]),
            str(flask.request.form["d_answer"]),
            str(quiz_id),
        ],
    )
    return flask.redirect("/teachers/quizzes/set/%s/" % (quiz_id))


#the following method may be modified or removed in future
@app.route("/teachers/grades/add/<class_id>/", methods=["POST"])
@db.validate_teacher
def create_grade(class_id):
    """ add a grade """
    db.insert_db(
        "INSERT INTO assignment_grades (student_id, assignment_id, grade) "
        "VALUES (?, ?, ?);",
        [
            flask.request.form["student"],
            flask.request.form["assignment"],
            flask.request.form["grade"],
        ],
    )
    flask.flash("Grade submitted.")
    return flask.redirect("/teachers/class/%s/" % (class_id))
