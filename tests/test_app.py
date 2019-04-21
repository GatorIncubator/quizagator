""" basic tests """
import pytest

from application import app
from application import login



def test_app_created():
    """Start with a blank database."""
    assert app is not None
