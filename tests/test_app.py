""" basic tests """
import pytest

from application import app


def test_app_created():
    """Start with a blank database."""
    assert app is not None
