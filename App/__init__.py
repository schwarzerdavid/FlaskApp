from flask import Flask

from App.src.or_scheduler_api.or_scheduler_routes import or_scheduler_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(or_scheduler_api)
    return app