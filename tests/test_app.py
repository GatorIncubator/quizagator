"""Basic Tests"""
import pytest

from application import app as appfactory


@pytest.fixture()
def factory():
    """Create an app and its test client"""
    actual_app = appfactory.create_app()

    # pylint: disable=too-few-public-methods
    class Group:
        """Group of created objects"""

        app = actual_app
        client = actual_app.test_client()

    return Group


# pylint: disable=redefined-outer-name
def test_app_created(factory):
    """Start with a blank database"""
    assert factory.app is not None


# pylint: disable=redefined-outer-name
def test_index(factory):
    """Test index page works -- NOT CORRECT"""
    res = factory.client.get("/")
    assert res.status_code == 404
    assert b"" in res.data
