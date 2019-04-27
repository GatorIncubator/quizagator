"""Basic Tests"""
import pytest

from application import app as appfactory

@pytest.fixture()
def app_client() {
    app = appfactory.create_app()

    
}

def test_app_created():
    """Start with a blank database."""
    assert app is not None


def test_index(app):
    res = app.get("/")
    # print(dir(res), res.status_code)
    assert res.status_code == 200
    assert b"" in res.data
