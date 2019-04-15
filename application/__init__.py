""" Application package initializer """
import flask

# main flask instance
app = flask.Flask(__name__)


from . import index
from . import db_connect
from . import students
from . import teachers
from . import login
