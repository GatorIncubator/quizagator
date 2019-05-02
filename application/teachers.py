""" teacher endpoints """
import csv
import os
import flask

from flask import current_app as app
from . import db_connect as db


MULTIPLE_CHOICE_OPTIONS = ["A", "B", "C", "D"]


@app.route("/teachers/")
@db.validate_teacher
def teachers():
    """ main teacher page """
    db.db_init()
    return flask.render_template("/teachers/index.html", classes=db.get_teacher_class())


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
        "SELECT class_id, name FROM classes order by class_id desc limit 1", one=True
    )
    flask.flash(
        f"Your class, {class_data[1]}, was created with an id of {class_data[0]}."
    )
    return flask.redirect("/teachers/")


@app.route("/teachers/classes/<class_id>/")
@db.validate_teacher
def class_page(class_id):
    """ specific class page """
    class_name = db.query_db("SELECT name FROM classes WHERE class_id=?", [class_id])
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
        "/teachers/quizzes/index.html", quizzes=db.get_quiz_teacher()
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
        reader = csv.reader(
            contents.splitlines(),
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True,
        )

        quiz_name = os.path.splitext(os.path.basename(str(file.filename)))[0]

        # TODO: associate quiz with class -- fix template to include form

        # create quiz metadata
        db.insert_db("INSERT INTO quizzes (name) VALUES (?)", [quiz_name])
        quiz_id = db.query_db("SELECT quiz_id FROM quizzes WHERE name=?;", [quiz_name])

        csv_entries = []
        for line in reader:
            entry = (
                quiz_id,  # quiz_id
                line[0],  # question_type
                line[1],  # question_text
                line[2],  # a_answer_text
                line[3],  # b_answer_text
                line[4],  # c_answer_text
                line[5],  # d_answer_text
                line[6],  # correct_answer (regex or letter)
            )
            csv_entries.append(entry)
        for entry in csv_entries:
            db.insert_db(
                "INSERT INTO questions (quiz_id, question_type, question_text,"
                " a_answer_text, b_answer_text, c_answer_text, d_answer_text,"
                " correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                entry,
            )
        return flask.redirect(f"/teachers/quizzes/{quiz_id}")
    flask.flash("file type not allowed")
    return flask.redirect(flask.request.url)


@app.route("/teachers/quizzes/<quiz_id>/")
@db.validate_teacher
def quiz_page(quiz_id):
    """Individual quiz page"""
    questions_db = db.query_db(
        "SELECT question_type, question_text, a_text, b_text, "
        "c_text, d_text, correct_answer FROM questions WHERE quiz_id=?;",
        [quiz_id],
    )
    questions = []
    for question in questions_db:

        question_info = {}
        question_info["type"] = question[0]
        question_info["text"] = question[1]
        # if this is a multiple-choice question
        if question[0] == 1:
            question_info["a"] = question[2]
            question_info["b"] = question[3]
            question_info["c"] = question[4]
            question_info["d"] = question[5]
        questions.append(question_info)

    quiz_name = db.query_db("SELECT name FROM quizzes WHERE quiz_id=?;", [quiz_id])

    return flask.render_template(
        "/students/quiz_page.html",
        quiz_id=quiz_id,
        questions=questions,
        quiz_name=str(quiz_name[0][0]),
    )
