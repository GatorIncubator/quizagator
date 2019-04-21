from flask import Flask, url_for, request, render_template

UPLOAD_FOLDER = '/teachers/classes/uploads/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from application import db_connect
import application.index
import application.students
import application.teachers
import application.login
