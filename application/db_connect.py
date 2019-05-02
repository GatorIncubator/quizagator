""" Describes the database connection """
import os
import functools
import sqlite3
import flask

from flask import current_app as app
from flask import g as context_globals


def db_init():
    """ Checks if database is already initialized, if not, create new one """
    database_path = app.config["DATABASE"]
    if not os.path.exists(database_path):
        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        # Create table - people
        c.execute(
            """CREATE TABLE people(
            person_id INTEGER PRIMARY KEY,
            isTeacher INTEGER,
            username TEXT,
            password TEXT,
            salt TEXT,
            name TEXT,
            email TEXT
            )"""
        )

        # Create table - classes
        c.execute(
            """CREATE TABLE classes(
            class_id INTEGER PRIMARY KEY,
            teacher_id INTEGER,
            name TEXT,
            FOREIGN KEY(teacher_id)
            REFERENCES people(person_id)
            )"""
        )

        c.execute(
            """CREATE TABLE quizzes(
            quiz_id INTEGER PRIMARY KEY,
            creator_id INTEGER,
            class_id INTEGER,
            name text,
            FOREIGN KEY(creator_id)
            REFERENCES people(person_id),
            FOREIGN KEY(class_id)
            REFERENCES classes(class_id)
            )"""
        )

        c.execute(
            """CREATE TABLE roster(
            roster_id INTEGER PRIMARY KEY,
            person_id INTEGER,
            class_id INTEGER,
            FOREIGN KEY(person_id)
            REFERENCES people(person_id),
            FOREIGN KEY (class_id)
            REFERENCES classes(class_id)
            )"""
        )

        c.execute(
            """CREATE TABLE questions(
            question_id INTEGER PRIMARY KEY,
            quiz_id INTEGER
            question_type INTEGER,
            question_text TEXT,
            a_answer_text TEXT,
            b_answer_text TEXT,
            c_answer_text TEXT,
            d_answer_text TEXT,
            correct_answer TEXT,
            response TEXT,
            FOREIGN KEY(quiz_id)
            REFERENCES quizzes(quiz_id)
            )"""
        )

        c.execute(
            """CREATE TABLE quiz_grades(
            grade_id INTEGER PRIMARY KEY,
            student_id integer,
            quiz_id INTEGER,
            grade REAL,
            FOREIGN KEY(student_id)
            REFERENCES people(person_id),
            FOREIGN KEY(quiz_id)
            REFERENCES quizzes(quiz_id)
            )"""
        )

        conn.commit()
        return conn
    return sqlite3.connect(database_path)


def get_db():
    """ Get database """
    if "db" not in context_globals:
        context_globals.db = db_init()

    return context_globals.db


@app.teardown_appcontext
def teardown_db(exception=None):
    """ Close database connection """
    if exception is not None:
        print(f"ERROR: {exception}")
    db = context_globals.pop("db", None)

    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """ Query database """
    cur = get_db().execute(query, args)
    returnval = cur.fetchall()
    cur.close()
    return (returnval[0] if returnval else None) if one else returnval


def insert_db(query, args=()):
    """ Insert into the database """
    db = get_db()
    db.execute(query, args)
    db.commit()


#################
# STUDENT FUNCS #
#################


def validate_student(func):
    """
    Checks to make sure the login is a student; if not,
    return route to teacher. Otherwise, return given function
    """

    @functools.wraps(func)
    def f(*args, **kwds):
        if "isTeacher" not in flask.session:
            return flask.redirect("/")
        if flask.session["isTeacher"] == 1:
            return flask.redirect("/teachers/")
        return func(*args, **kwds)

    return f


def get_student_classes():
    """ Get classes for student """
    class_data = query_db(
        "SELECT classes.class_id, classes.name FROM classes JOIN roster "
        "ON roster.class_id=classes.class_id where person_id=?;",
        [flask.session["id"]],
    )
    classes = []
    for class_info in class_data:
        student_class = {}
        student_class["id"] = class_info[0]
        student_class["name"] = class_info[1]
        classes.append(student_class)
    return classes


def get_student_grade(class_id):
    """ Gets all the grades given to the student """
    grades = []
    quiz_grade = query_db(
        "SELECT quizzes.name, grade FROM quiz_grades JOIN quizzes "
        "ON quiz_grades.quiz_id=quizzes.quiz_id "
        "WHERE student_id=? AND quizzes.class_id=?;",
        [flask.session["id"], class_id],
    )
    for grade in quiz_grade:
        student_grade_quiz = {}
        student_grade_quiz["quiz_name"] = grade[0]
        student_grade_quiz["grade"] = grade[1]
        grades.append(student_grade_quiz)
    return grades


def validate_teacher(func):
    """
    Checks to make sure the login is a teacher; if not,
    return route to student. Otherwise, return given function
    """

    @functools.wraps(func)
    def f(*args, **kwds):
        if "isTeacher" not in flask.session:
            return flask.redirect("/")
        if flask.session["isTeacher"] == 0:
            return flask.redirect("/students/")
        return func(*args, **kwds)

    return f


def get_teacher_class():
    """ Gets the classes from a teacher's class_data """
    class_data = query_db(
        "SELECT class_id, name FROM classes WHERE teacher_id=?;", [flask.session["id"]]
    )
    classes = []
    for part in class_data:
        class_dict = {}
        class_dict["id"] = part[0]
        class_dict["name"] = str(part[1])
        classes.append(class_dict)
    return classes


def get_quiz_teacher():
    """ Get quizzes created by the current teacher """
    quiz_data = query_db(
        "SELECT quiz_id, name FROM quizzes WHERE creator_id=?;", [flask.session["id"]]
    )
    quizzes = []
    for quiz in quiz_data:
        quiz_dict = {}
        quiz_dict["id"] = quiz[0]
        quiz_dict["name"] = quiz[1]
        quizzes.append(quiz_dict)
    return quizzes


def get_class_quiz(class_id):
    """ Get quizzes for a specified class """
    quiz_data = query_db(
        "SELECT quiz_id, name FROM quizzes WHERE class_id=?;", [class_id]
    )
    quizzes = []
    for quiz in quiz_data:
        quiz_class = {}
        quiz_class["id"] = quiz[0]
        quiz_class["name"] = quiz[1]
        quizzes.append(quiz_class)
    return quizzes


def get_students_class(class_id):
    """ Get all the students in a specified class """
    student_data = query_db(
        "SELECT people.person_id, name FROM people JOIN roster "
        "ON roster.person_id=people.person_id WHERE roster.class_id=?;",
        [class_id],
    )
    student_class = []
    for student in student_data:
        student_dict = {}
        student_dict["id"] = student[0]
        student_dict["name"] = student[1]
        student_class.append(student_dict)
    return student_class


def get_class_grades(class_id):
    """ Get grades given to students in a specified class """

    grades = []
    quiz_grades = query_db(
        "SELECT people.name, quizzes.name, grade FROM quiz_grades JOIN people "
        "ON quiz_grades.student_id=people.person_id JOIN quizzes "
        "ON quiz_grades.quiz_id=quizzes.quiz_id WHERE quizzes.class_id=?;",
        [class_id],
    )
    for grade in quiz_grades:
        grade_class = {}
        grade_class["student_name"] = grade[0]
        grade_class["quiz_name"] = grade[1]
        grade_class["grade"] = grade[2]
        grades.append(grade_class)
