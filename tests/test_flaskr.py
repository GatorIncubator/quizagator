""" basic tests """
import pytest


@pytest.fixture
def client():
    """ client fixture """

    yield {"DATABASE": None, "TESTING": True}


# pylint: disable=redefined-outer-name
def test_empty_db(client):
    """Start with a blank database."""
    assert client["DATABASE"] is None
