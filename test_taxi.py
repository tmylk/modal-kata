import pytest

from taxi import get_data, stub

@pytest.fixture(scope="session", autouse=True)
def app():
    with stub.run() as app:
        yield app
        
def test_get_data():
    assert get_data.call(2) == 4

