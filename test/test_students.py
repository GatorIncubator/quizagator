"""Test cases for the login.py"""
# pylint: disable=unused-import
import pytest
from application import login


def test_login_teacher(input_freq):
    """ Tests if logs in as teacher """
    user = "student_present"
    password = "pass"
    storage_manager_freq = compute_tf_objectoriented.WordFrequencyManager()
    for item in input_freq:
        storage_manager_freq.increment_count(input_freq[i])
        i += 1
    word_freq_list = storage_manager_freq.sorted()
    assert word_freq_list == [("cow", 2), ("moo", 1)]
