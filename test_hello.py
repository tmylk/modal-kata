import pytest
from modal import Stub

from get_started import f_local, run_f


def test_local():
    assert f_local(2) == 4

def test_global():
    assert run_f(2) == 4
    