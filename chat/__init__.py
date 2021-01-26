from flask_socketio import SocketIO

from flask import Flask

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    socketio.init_app(app)

    from chat.views import bp_main
    app.register_blueprint(bp_main, url_prefix='/')

    from chat.events.messages import bp_message
    app.register_blueprint(bp_message, url_prefix='/chat')

    return app
