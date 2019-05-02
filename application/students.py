""" Student endpoints """
import flask

from flask import current_app as app
from . import db_connect as db


@app.route("/students/")
@db.validate_student
def student_home():
    """ student default page """
    return flask.render_template(
        "/students/index.html", classes=db.get_student_classes()
    )


@app.route("/students/classes/")
@db.validate_student
def student_classes_home():
    """ student classes page """
    return flask.render_template(
        "/students/classes.html", classes=db.get_student_classes()
    )


@app.route("/students/classes/join/", methods=["POST"])
@db.validate_student
def student_class_join():
    """If student joins a class"""
    db.insert_db(
        "INSERT INTO roster (people_id, class_id) VALUES (?, ?);",
        [flask.session["id"], flask.request.form["id"]],
    )
    flask.flash(f"You joined the class with an id of {flask.request.form["id"]}")
    return flask.redirect("/students/classes")


@app.route("/students/class/<class_id>/")
@db.validate_student
def student_class_page(class_id):
    """ shows classes """
    class_name = db.query_db(
        "SELECT name FROM classes WHERE id=?;", [class_id], one=True
    )
    return flask.render_template(
        "/students/class_page.html",
        class_name=str(class_name[0]),
        topics=db.get_class_topic(class_id),
        assignments=db.get_class_assign(class_id),
        quizzes=db.get_class_quiz(class_id),
        grades=db.get_student_grade(class_id),
    )


@app.route("/students/quizzes/<quiz_id>/")
@db.validate_student
def student_quiz_page(quiz_id):
    """Allows students to view/take quizzes"""
    quiz_name = db.query_db("SELECT name FROM quizzes WHERE id=?;", [quiz_id])
    result = db.query_db(
        "SELECT grade from quiz_grades WHERE quiz_id=? AND student_id=?;",
        [quiz_id, flask.session["id"]],
        one=True,
    )  # check if the person has already taken the test
    if result is None:
        questions_db = db.query_db(
            "SELECT id, question_text, a_answer_text, b_answer_text, c_answer_text, "
            "d_answer_text FROM questions WHERE quiz_id=?;",
            [quiz_id],
        )
        items = []
        for question in questions_db:
            question_dict = {}
            question_dict["id"] = question[0]
            question_dict["text"] = question[1]
            if question[2] is not None:
                question_dict["answers"] = [
                    str(question[2]),
                    str(question[3]),
                    str(question[4]),
                    str(question[5]),
                ]
            else:
                questions_db = db.query_db(
                    "SELECT id, question_text, "
                    "open_question FROM questions WHERE quiz_id=?;"[quiz_id]
                )
                question_dict["answer"] = [str(question[2])]
            items.append(question_dict)
        return flask.render_template(
            "/students/quiz_page.html",
            items=items,
            quiz_name=quiz_name[0][0],
            quiz_id=quiz_id,
        )
    flask.flash("You receieved a grade of {0}% on this quiz.".format(result[0]))
    return flask.render_template("/students/quiz_page.html", quiz_name=quiz_name[0][0])


@app.route("/students/assignments/<assignment_id>/")
@db.validate_student
def student_assignment_page(assignment_id):
    """ specified assignment page for a student """
    assignment_data = db.query_db(
        "SELECT name, description, due_date FROM assignments WHERE id=?;",
        [assignment_id],
        one=True,
    )
    name = assignment_data[0]
    description = assignment_data[1]
    due_date = assignment_data[2]
    return flask.render_template(
        "/students/assignment_page.html",
        name=name,
        description=description,
        due_date=due_date,
    )
