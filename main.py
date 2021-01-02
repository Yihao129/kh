from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send, emit
from flask_cors import cross_origin, CORS
from functions import *

total_online = 0

app = Flask(__name__, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')



@socketio.on('message')
def handleMessage(msg):
    print("got message")
    msg = decodeMsg(msg)
    print('Message: ' + msg["msg"])
    send(msg, broadcast=True)

   
@socketio.on('connect')
def handleConnect():
    print("A user comes.")
    global total_online
    total_online += 1
    print("current total:", total_online)
    emit("updateOnlineCount", total_online, broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    print("A user leaves.")
    global total_online
    total_online -= 1
    print("emitting total")
    emit("updateOnlineCount", total_online, broadcast=True)

@cross_origin()
@app.route('/', methods=['GET', 'POST'])
def home():
    print(request.remote_addr, "**********************")
    return render_template('index.html')

@app.route('/lib/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('lib', path)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80)
