from flask_socketio import join_room,rooms
from project import socketio as sio
from flask_login import login_required, current_user
from flask import render_template, redirect, session, Blueprint, url_for, request

chat = Blueprint('chat', __name__, template_folder='templates')


@chat.route('/chat')
@login_required
def chat_page():
    room_id = session.get('room_id')
    if not room_id:
        return redirect(url_for('user.welcome'))
    return render_template('chat/chat.html', room=room_id)


@sio.event
def room_join(data):
    join_room(data['room_id'])
    sio.emit('user_join_alert', data)

@sio.event
def send_message(data):
    sio.emit('recive_message', data, to=data['room_id'])

@sio.event
def disconnect():
    sid = request.sid
    room = rooms(sid)
    room.remove(sid)
    room = room[0]
    sio.emit('user_left_alert', current_user.username, room=room)