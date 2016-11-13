# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from utils.common_utils import format_datetime

from utils.common_utils import now_lambda

__author__ = 'fleago'


from flask import Flask, render_template, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_string(msg):
    print 'got %s' % msg


@socketio.on('connect')
def handle_message():
    print('somebody connect this, %s' % format_datetime(now_lambda()))


@socketio.on('new arrival')
def handle_message_arrival(data):
    print('got message %s, %s' % (data['message'], format_datetime(now_lambda())))
    emit('notice', {'message': '欢迎新用户到来 %d' % random.randint(1, 1000)}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    print '断开了链接'


@socketio.on('set nickname')
def set_nickname(nickname):
    session['nickname'] = nickname
    # emit('notice', {'message': '昵称设置为%s' % nickname})
    emit('nickname ready', nickname, callback=ack)
    return 'ganggang'

def ack():
    print 'message was received'


@socketio.on('chat')
def chat(data):
    nickname = session['nickname']
    emit('notice', {'message': '%s: %s' % (nickname, data['message'])}, broadcast=True)


# @socketio.on('my event')
# def handle_message(message):
#     print('received message: ' + message)
#     return 'server got ' + message

#
# @socketio.on('json')
# def handle_json(json):
#     print('received json: ' + str(json))
#
#
# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#     return 'server received json data %s' % str(json)
#
#
# @socketio.on('notice')
# def notice():
#     return {'message': 'a big day for sale'}


# @socketio.on('my event')
# def handle_my_custom_event(arg1, arg2, arg3):
#     print('received args: ' + arg1 + arg2 + arg3)
#
#
# @socketio.on('my event', namespace='/test')
# def handle_my_custom_namespace_event(json):
#     print('received json: ' + str(json))
#
#
# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#     return 'one', 2


if __name__ == '__main__':
    socketio.run(app, port=5003, debug=True)
