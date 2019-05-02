""" teacher endpoints """
import csv
import os
import re
import flask

from flask import current_app as app
from .students import student_quiz_page
from . import db_connect as db

# routes once teacher has been validated to point to different html pages

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
        "SELECT class_id, name FROM classes ORDER BY class_id DESC LIMIT 1", one=True
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
        quizzes=db.get_class_quizzes(class_id),
        students=db.get_class_students(class_id),
        grades=db.get_class_grades(class_id),
    )


@app.route("/teachers/classes/<class_id>/quizzes/create/", methods=["GET", "POST"])
@db.validate_teacher
def upload_quiz(class_id):
    """Upload a quiz csv with POST or see the upload page with GET"""
    if flask.request.method != "POST":
        return flask.render_template("/teachers/quizzes/create.html", class_id=class_id)

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

        csv_entries = []
        for line in reader:
            entry = [
                int(line[0]),  # question_type
                line[1],  # question_text
                line[2],  # a_text
                line[3],  # b_text
                line[4],  # c_text
                line[5],  # d_text
                line[6],  # correct_answer (regex or letter)
            ]

            valid = True
            if entry[0] != 0 and entry[0] != 1:
                flask.flash("Invalid CSV: Question type can only be 0 or 1")
                valid = False
            if len(entry[6]) == 1 and entry[6].upper() not in "ABCD":
                flask.flash(
                    "Invalid CSV: Correct answer should be 'A', 'B', 'C', or"
                    " 'D'; if it is a regex, it should be more than"
                    " a single character"
                )
                valid = False
            if len(entry[6]) > 1:
                try:
                    re.compile(entry[6])
                except re.error:
                    flask.flash("Invalid CSV: Correct answer regex is not valid")
                    valid = False

            if not valid:
                return flask.redirect(flask.request.url)

            csv_entries.append(entry)

        # create quiz metadata
        quiz_name = os.path.splitext(os.path.basename(str(file.filename)))[0]
        db.insert_db(
            "INSERT INTO quizzes (creator_id, class_id, name) VALUES (?, ?, ?)",
            [flask.session["id"], class_id, quiz_name],
        )
        quiz_id = db.query_db(
            "SELECT quiz_id FROM quizzes WHERE creator_id=? AND class_id=?"
            " AND name=? ORDER BY quiz_id DESC LIMIT 1;",
            [flask.session["id"], class_id, quiz_name],
            one=True,
        )[0]

        for entry in csv_entries:
            db.insert_db(
                "INSERT INTO questions (quiz_id, question_type, question_text,"
                " a_text, b_text, c_text, d_text, correct_answer)"
                f"VALUES ({quiz_id}, ?, ?, ?, ?, ?, ?, ?);",
                entry,
            )
        return flask.redirect(f"/teachers/classes/{class_id}/quizzes/{quiz_id}")
    flask.flash("file type not allowed")
    return flask.redirect(flask.request.url)


@app.route("/teachers/classes/<class_id>/quizzes/<quiz_id>/")
@db.validate_teacher
def quiz_page(class_id, quiz_id):
    """Individual quiz page"""
    return student_quiz_page.__wrapped__(class_id, quiz_id)
