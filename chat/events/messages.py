from flask import Blueprint, render_template, request, session, url_for
from flask_socketio import emit, join_room, leave_room
from werkzeug.utils import redirect

from chat import socketio

bp_message = Blueprint('message', __name__)


@bp_message.route('/')
def join():
    return render_template('join.html')


@bp_message.route('/room', methods=['GET', 'POST'])
def room():
    data = request.json
    session['nick'] = data['nick']
    session['room'] = data['room']
    return 'ok'


@bp_message.route('/chat')
def chat():
    nick = session.get('nick', '')  # empty string because we don't want None
    room = session.get('room', '')

    if nick == '' or room == '':
        return redirect(url_for('message.join'))

    return render_template('chat.html', nick=nick, room=room)


@socketio.on('message', namespace='/chat')  # listen for events 'message'
def handle_message(message):
    print(message)
    room = session.get('room', '')
    emit('message', {'msg': f"{message['nick']}: {message['msg']}"}, namespace='/chat', broadcast=True, room=room)  # emit event, payload parameter {}


@socketio.on('joined', namespace='/chat')  # namespace is only for websocket (zeby podzielic kilka funkcji w jednym polaczeniu/jednym websockecie)
def handle_connect(connect):
    print(connect)
    join_room(session.get('room', ''))  # to connect to room


@socketio.on('left', namespace='/chat')
def close_connect(connect):
    leave_room(session.get('room', ''))
