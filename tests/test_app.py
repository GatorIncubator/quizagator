"""Basic Tests"""
import pytest

from application import app as appfactory


@pytest.fixture()
def factory():
    actual_app = appfactory.create_app()

    class Group:
        app = actual_app
        client = actual_app.test_client()

    return Group


def test_app_created(factory):
    """Start with a blank database"""
    assert factory.app is not None


def test_index(factory):
    """Test index page works -- NOT CORRECT"""
    res = factory.client.get("/")
    assert res.status_code == 404
    assert b"" in res.data
