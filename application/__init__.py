from flask import Flask, url_for, request, render_template
app = Flask(__name__)

from application import db_connect
import application.index
import application.students
import application.teachers
import application.login
