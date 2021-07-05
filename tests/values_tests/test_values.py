from shorty.app import create_app
from pyshorteners import Shortener
from shorty.validators import Provider
import pytest


shortener = Shortener(api_key='0c4850b19247b4d208f409d93255ee3221454ecb')


@pytest.fixture
def app():
    app = create_app(settings_overrides=dict(TESTING=True))
    return app


@pytest.fixture(scope='function')
def client(app, request):
    return app.test_client()


def test_main_ref_for_first_provider(client):
    response = client.post('/shortlinks', json={'url': "http://www.google.com", "provider": Provider.tinyurl})
    assert response.json['url'] == 'http://www.google.com'


def test_main_ref_for_second_provider(client):
    response = client.post('/shortlinks', json={'url': "http://www.google.com", "provider": Provider.bitly})
    assert response.json['url'] == 'http://www.google.com'


def test_ref_reverse_for_first_provider(client):
    response = client.post('/shortlinks', json={'url': "http://www.google.com/", "provider": Provider.tinyurl})
    assert shortener.tinyurl.expand(response.json['link']) == "http://www.google.com/"


def test_ref_reverse_for_second_provider(client):
    response = client.post('/shortlinks', json={'url': "http://www.google.com/", "provider": Provider.bitly})
    assert shortener.bitly.expand(response.json['link']) == 'http://www.google.com/'
