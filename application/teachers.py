""" teacher endpoints """
import csv
import flask

from flask import current_app as app
from . import db_connect as db


@app.route("/teachers/")
@db.validate_teacher
def teachers():
    """ main teacher page """
    db.db_init()
    return flask.render_template("/teachers/index.html", classes=db.get_teacher_class())


@app.route("/teachers/classes/")
@db.validate_teacher
def classes_page():
    """ teacher's class list """
    return flask.render_template(
        "/teachers/classes/index.html", classes=db.get_teacher_class()
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


@app.route("/teachers/classes/<class_id>/")
@db.validate_teacher
def class_page(class_id=None):
    """ specific class page """
    class_name = db.query_db("SELECT name FROM classes WHERE id=?", [class_id])
    class_name = class_name[0][0]
    return flask.render_template(
        "/teachers/classes/class_page.html",
        class_id=class_id,
        class_name=class_name,
        students=db.get_students_class(class_id),
    )


@app.route("/teachers/quizzes/")
@db.validate_teacher
def quizzes_page():
    """Main teacher quiz list page"""
    return flask.render_template(
        "/teachers/quizzes/index.html",
        topics=db.get_teacher_topic_all(),
        quizzes=db.get_quiz_teacher(),
    )


@app.route("/teachers/quizzes/create/", methods=["GET", "POST"])
@db.validate_teacher
def upload_quiz():
    """Upload a quiz csv with POST or see the upload page with GET"""
    if flask.request.method != "POST":
        return flask.render_template(
            "/teachers/quizzes/create.html", quizzes=db.get_quiz_teacher()
        )

    # check if the post request has the file part
    if "file" not in flask.request.files:
        flask.flash("No file part")
        return flask.redirect(flask.request.url)
    file = flask.request.files["file"]
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == "":
        flask.flash("No selected file")
        return flask.redirect(flask.request.url)
    if file and file.filename.endswith(".csv"):
        contents = file.stream.read().decode("utf-8")
        reader = csv.reader(contents)
        questionArray = []
        quizID = 4
        for line in reader:
            questionLine = (
                "",
                line[0],
                line[1],
                line[2],
                line[3],
                line[4],
                line[5],
                line[6],
                line[7],
                line[8],
                line[9],
                quizID,
            )
            questionArray.append(questionLine)
            print(questionArray)
        for i in questionArray:
            #    INSERT INTO questions
            #    VALUES
            #    (i);
            print(i)  # ENDS INSERT INTO DB
        return flask.redirect("/teachers/quizzes/")
    flask.flash("file type not allowed")
    return flask.redirect(flask.request.url)


@app.route("/teachers/quizzes/<quiz_id>/")
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

    quiz_name = db.query_db("SELECT name FROM quizzes WHERE id=?;", [quiz_id])

    return flask.render_template(
        "/teachers/quizzes/quiz_page.html",
        quiz_id=quiz_id,
        questions=questions,
        quiz_name=str(quiz_name[0][0]),
    )
