from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send
from flask_cors import cross_origin, CORS
from urllib.parse import unquote


app = Flask(__name__, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
    print("got message")
    m = unquote(unquote(msg))
    print('Message: ' + m)
    send(msg, broadcast=True)


@cross_origin()
@app.route('/', methods=['GET', 'POST'])
def home():
    print("in")
    return render_template('index.html')

@app.route('/lib/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('lib', path)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port="80")
