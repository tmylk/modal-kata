import pytest

from square import f, stub


@pytest.fixture(scope="session", autouse=True)
def app():
    with stub.run() as app:
        yield app
        
def test_first_modal_test():
    assert f.call(2) == 4

def test_second_modal_test():
    assert f.call(3) == 9

def test_local():
    f_local =f.get_raw_f()
    assert f_local(2) == 4
