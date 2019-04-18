""" Application package initializer """
import flask

# main flask instance
app = flask.Flask(__name__)

# pylint: disable=wrong-import-position
from . import index  # noqa: E402, F401
from . import db_connect  # noqa: E402, F401
from . import students  # noqa: E402, F401
from . import teachers  # noqa: E402, F401
from . import login  # noqa: E402, F401
