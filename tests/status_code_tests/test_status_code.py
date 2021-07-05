from shorty.app import create_app
from shorty.validators import Provider
import pytest


@pytest.fixture
def app():
    app = create_app(settings_overrides=dict(TESTING=True))
    return app


@pytest.fixture(scope='function')
def client(app, request):
    return app.test_client()


def test_not_found1(client):
    assert client.get('/') == 404


def test_not_found2(client):
    assert client.get('/bad_ref') == 404


def test_method_not_allowed1(client):
    assert client.get('/shortlinks') == 405


def test_method_not_allowed2(client):
    assert client.put('/shortlinks') == 405


def test_bad_provider(client):
    assert client.post('/shortlinks', json={'url': "'http://www.google.com'", "provider": "blabla"}) == 400


def test_first_provider(client):
    assert client.post('/shortlinks', json={'url': "http://www.google.com", "provider": Provider.bitly}) == 200


def test_second_provider(client):
    assert client.post('/shortlinks', json={'url': "'http://www.google.com'", "provider": Provider.tinyurl}) == 200


def test_ok(client):
    assert client.post('/shortlinks', json={'url': "'http://www.google.com'"}) == 200
