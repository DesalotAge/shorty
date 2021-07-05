from flask import Flask
from shorty.api import ShortifyView
from flask_restful import Api
from flasgger import Swagger


def create_app(settings_overrides=None):
    """
    creating app and configuration
    :param settings_overrides:
    :return:
    """
    app = Flask(__name__)
    configure_settings(app, settings_overrides)
    configure_swagger(app)
    configure_api(app)
    return app


def configure_settings(app, settings_override):
    """
    add configurations
    :param app:
    :param settings_override:
    :return:
    """
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
    })
    if settings_override:
        app.config.update(settings_override)


def configure_api(app):
    """
    configurates all api-structures
    :param app:
    :return:
    """
    api = Api(app)
    api.add_resource(ShortifyView, '/shortlinks')


def configure_swagger(app):
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Flask Restful Swagger Demo",
            "description": "A Demof for the Flask-Restful Swagger Demo",
            "version": "0.1.1",
            "contact": {
                "name": "Kanoki",
                "url": "https://Kanoki.org",
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {"
                               "token}\" "
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]

    }
    app.config['SWAGGER'] = {
        'title': 'My API',
        'uiversion': 3,
        "specs_route": "/swagger/"
    }
    swagger = Swagger(app, template=template)