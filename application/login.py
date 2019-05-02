""" Login page, handles student and teacher usernames, passwords, and registration """
import flask

from flask import current_app as app
from . import db_connect

# Handles login information and cross checks login information with DB


@app.route("/login/", methods=["POST"])
def login():
    """Log in the student or teacher"""
    # get form information
    form_data = flask.request.form

    # validation
    if form_data["username"] == "":
        flask.flash("The username field is required.")
        return flask.redirect("/")
    if form_data["password"] == "":
        flask.flash("The password field is required.")
        return flask.redirect("/")

    # get data from database
    data = db_connect.query_db(
        "SELECT password, isTeacher, person_id FROM people WHERE username=? LIMIT 1",
        [form_data["username"]],
    )
    # make sure username is right
    if data == []:
        flask.flash("Your username was incorrect.")
        return flask.redirect("/")

    # check the password
    user_pass = form_data["password"]
    if data[0][0] == user_pass:
        # correct password
        flask.session["isTeacher"] = data[0][1]
        flask.session["id"] = data[0][2]
        # if student, redirect to students page
        if flask.session["isTeacher"] == 0:
            return flask.redirect("/students/")
        # else they are a teacher, redirect to teachers page
        return flask.redirect("/teachers/")

    flask.flash("Your password was incorrect.")
    return flask.redirect("/")


@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register the user"""
    # form data is GET, so render template
    if flask.request.method == "GET":
        return flask.render_template("register.html")

    # request method is POST, so do everything

    form_data = flask.request.form

    # form validation
    # pylint: disable=bad-continuation
    if (
        form_data["username"] == ""
        or form_data["password"] == ""
        or form_data["name"] == ""
        or form_data["email"] == ""
    ):
        return "All text fields are required"
    if "isTeacher" not in form_data:
        isTeacher = 0  # they are not a teacher
    else:
        isTeacher = 1  # they are a teacher

    password = form_data["password"]
    db_connect.insert_db(
        "INSERT INTO people (isTeacher, username, password, name, email)"
        "VALUES (?, ?, ?, ?, ?)",
        [
            isTeacher,
            form_data["username"],
            password,
            form_data["name"],
            form_data["email"],
        ],
    )
    flask.flash("The entry was created")
    return flask.redirect("/")
