from flask import Flask


def create_app():
    app = Flask(__name__)

    from chat.views import bp_main
    app.register_blueprint(bp_main, url_prefix='/')

    return app
