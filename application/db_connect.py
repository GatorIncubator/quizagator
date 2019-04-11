""" Describes the database connection """

import functools
import sqlite3
import flask

# from flask import g, session, escape
from application import app


DATABASE = "database.db"


def get_db():
    """ Get database """
    db = getattr(flask.g, "_database", None)
    if db is None:
        db = flask.g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
# pylint: disable=unused-argument
def close_connection(exception):
    """ Close database connection """
    db = getattr(flask.g, "_database", None)
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
        "SELECT classes.id, classes.name FROM classes JOIN roster "
        "ON roster.class_id = classes.id where people_id=?;",
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
        "ON quiz_grades.quiz_id=quizzes.id JOIN topics "
        "ON quizzes.topic_id=topics.id JOIN classes "
        "ON topics.class_id=classes.id "
        "WHERE student_id=? AND topics.class_id=?;",
        [flask.session["id"], class_id],
    )
    for grade in quiz_grade:
        student_grade_quiz = {}
        student_grade_quiz["thing_name"] = grade[0]
        student_grade_quiz["grade"] = grade[1]
        grades.append(student_grade_quiz)
    assignment_grade = query_db(
        "SELECT assignments.name, grade FROM assignment_grades "
        "JOIN assignments ON assignment_grades.assignment_id=assignments.id "
        "JOIN topics on assignments.topic_id=topics.id JOIN classes "
        "ON topics.class_id=classes.id WHERE student_id=? "
        "AND topics.class_id=?;",
        [flask.session["id"], class_id],
    )
    for grade in assignment_grade:
        student_grade_assignment = {}
        student_grade_assignment["thing_name"] = grade[0]
        student_grade_assignment["grade"] = grade[1]
        grades.append(student_grade_assignment)
    return grades


#################
# TEACHER FUNCS #
#################


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
        "SELECT id, name FROM classes WHERE teacher_id = ?;", [flask.session["id"]]
    )
    classes = []
    for part in class_data:
        class_dict = {}
        class_dict["id"] = part[0]
        class_dict["name"] = str(part[1])
        classes.append(class_dict)
    return classes


def get_teacher_topic_all():
    """ Get a teacher's topics """
    topic_data = query_db(
        "SELECT topics.id, topics.name, classes.name FROM topics JOIN classes "
        "ON topics.class_id=classes.id WHERE teacher_id=?;",
        [flask.session["id"]],
    )
    topics = []
    for topic in topic_data:
        topic_dict_teacher = {}
        topic_dict_teacher["id"] = topic[0]
        topic_dict_teacher["name"] = flask.escape(str(topic[1]))
        topic_dict_teacher["class"] = flask.escape(str(topic[2]))
        topics.append(topic_dict_teacher)
    return topics


def get_class_topic(class_id):
    """ Get all the topics in a specified class """
    topic_data = query_db("SELECT id, name FROM topics WHERE class_id=?", [class_id])
    topics = []
    for topic in topic_data:
        topic_dict_class = {}
        topic_dict_class["id"] = topic[0]
        topic_dict_class["name"] = topic[1]
        topics.append(topic_dict_class)
    return topics


def get_teacher_assign():
    """ Get all the assignments in teacher class """
    assignment_data = query_db(
        "SELECT assignments.id, assignments.name, assignments.due_date "
        "FROM assignments JOIN topics ON assignments.topic_id=topics.id "
        "JOIN classes ON topics.class_id=classes.id WHERE teacher_id=?;",
        [flask.session["id"]],
    )
    assignments = []
    for assignment in assignment_data:
        assignment_dict_teach = {}
        assignment_dict_teach["id"] = assignment[0]
        assignment_dict_teach["name"] = assignment[1]
        assignment_dict_teach["due_date"] = assignment[2]
        assignments.append(assignment_dict_teach)
    return assignments


def get_class_assign(class_id):
    """ Get all the assignments for a specified class """
    assignment_data = query_db(
        "SELECT id, name, due_date FROM assignments "
        "WHERE topic_id=(SELECT id FROM topics WHERE class_id=?);",
        [class_id],
    )
    assignments = []
    for assignment in assignment_data:
        assignment_dict_class = {}
        assignment_dict_class["id"] = assignment[0]
        assignment_dict_class["name"] = str(assignment[1])
        assignment_dict_class["due_date"] = assignment[2]
        assignments.append(assignment_dict_class)
    return assignments


def get_topic_assign(topic_id):
    """ Get assignments for a specified topic """
    assignment_data = query_db(
        "SELECT id, name, due_date FROM assignments WHERE topic_id=?;", [topic_id]
    )
    assignments = []
    for assignment in assignment_data:
        topic_assign_dict = {}
        topic_assign_dict["id"] = assignment[0]
        topic_assign_dict["name"] = str(assignment[1])
        topic_assign_dict["due_date"] = assignment[2]
        assignments.append(topic_assign_dict)
    return assignments


def get_quiz_teacher():
    """ Get quizzes created by the current teacher """
    quiz_data = query_db(
        "SELECT id, name FROM quizzes WHERE creator_id=?;", [flask.session["id"]]
    )
    quizzes = []
    for quiz in quiz_data:
        quiz_dict = {}
        quiz_dict["id"] = quiz[0]
        quiz_dict["name"] = quiz[1]
        quizzes.append(quiz_dict)
    return quizzes


def get_topic_quiz(topic_id):
    """ Get quizzes for a specified topic """
    quiz_data = query_db("SELECT id, name FROM quizzes WHERE topic_id=?;", [topic_id])
    quizzes = []
    for quiz in quiz_data:
        quiz_topic = {}
        quiz_topic["id"] = quiz[0]
        quiz_topic["name"] = quiz[1]
        quizzes.append(quiz_topic)
    return quizzes


def get_class_quiz(class_id):
    """ Get quizzes for a specified class """
    quiz_data = query_db(
        "SELECT quizzes.id, quizzes.name FROM quizzes JOIN topics "
        "ON topics.id=quizzes.topic_id WHERE topics.class_id=?;",
        [class_id],
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
        "SELECT people.id, name FROM people JOIN roster "
        "ON roster.people_id=people.id WHERE roster.class_id=?;",
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
        "ON quiz_grades.student_id=people.id JOIN quizzes "
        "ON quiz_grades.quiz_id=quizzes.id JOIN topics "
        "ON quizzes.topic_id=topics.id JOIN classes "
        "ON topics.class_id=classes.id WHERE classes.id=?;",
        [class_id],
    )
    for grade in quiz_grades:
        grade_class = {}
        grade_class["student_name"] = grade[0]
        grade_class["thing_name"] = str(grade[1]) + " (Quiz)"
        grade_class["grade"] = grade[2]
        grades.append(grade_class)
    assignment_grades = query_db(
        "SELECT people.name, assignments.name, grade FROM assignment_grades "
        "JOIN people ON assignment_grades.student_id=people.id "
        "JOIN assignments ON assignment_grades.assignment_id=assignments.id "
        "JOIN topics ON assignments.topic_id=topics.id JOIN classes "
        "ON topics.class_id=classes.id WHERE classes.id=?;",
        [class_id],
    )
    for grade in assignment_grades:
        grade_assign = {}
        grade_assign["student_name"] = grade[0]
        grade_assign["thing_name"] = str(grade[1]) + " (Assignment)"
        grade_assign["grade"] = grade[2]
        grades.append(grade_assign)
    return grades
