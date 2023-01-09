import pytest

from taxi import get_data, stub


@pytest.fixture(scope="session", autouse=True)
def app():
    with stub.run() as app:
        yield app
        
def test_get_data():
    l = get_data.call()
    assert len(l) > 0

def test_only_june_2022():
    l = get_data.call()
    for date, count in l:
        assert date.month == 6
        assert date.year == 2022

    
