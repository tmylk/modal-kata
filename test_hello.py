import pytest
from modal import Stub

from get_started import f, stub

# @pytest.fixture(scope="session", autouse=True)
# def stub():

#     # prepare something ahead of all tests
    

def test_local():
    f_local =f.get_raw_f()
    assert f_local(2) == 4

def test_two():
    with stub.run() as application:
        assert f.call(2) == 4

def test_three():
    with stub.run() as application:
        assert f.call(3) == 9
