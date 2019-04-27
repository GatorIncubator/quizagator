""" basic tests """
import pytest

from application import app
from application import login


def test_app_created():
    """Start with a blank database."""
    assert app is not None


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flaskr.app.config["DATABASE"] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()


# def test_index(app):
#     res = app.get("/")
#     # print(dir(res), res.status_code)
#     assert res.status_code == 200
#     assert b"" in res.data
