from time import sleep
import signal
from requests import post
from datetime import datetime
import time
import webbrowser
import sys
import os
import socket
from flask_socketio import SocketIO, disconnect
from flask_cors import CORS
from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv

load_dotenv()

base_dir = '.'
template_dir = '../frontend/dist/spa'
static_dir = '../frontend/dist/spa/assets'

if hasattr(sys, '_MEIPASS'):
    template_dir = os.path.join(sys._MEIPASS)
    static_dir = os.path.join(template_dir, 'assets')

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
CORS(app)
socketio = SocketIO(app)

token_api = os.getenv('TOKEN_API')
message_api = os.getenv('MESSAGE_API')
admin_info = {
    'username': os.getenv('NAME'),
    'password': os.getenv('PASSWORD'),
}
access_token = None


@app.get('/')
def get_app():
    global access_token
    try:
        if access_token is None:
            res = post(token_api, json=admin_info, timeout=5)
            res.raise_for_status()
            access_token = res.json()['access_token']
        return render_template('index.html')
    except Exception as e:
        signal.raise_signal(signal.SIGINT)
        return f"<h3>Internal server Error</h3> \
            <p style='color:red;'>{str(e)}</p>"


@app.route('/favicon.ico')
def get_favicon():
    return send_from_directory(template_dir, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


def disconnect_client():
    disconnect(sid=request.sid)


@socketio.on('connect')
def process_connect(auth):
    if auth['name'] != admin_info['username'] or \
            auth['pwd'] != admin_info['password']:
        socketio.emit('permission', {'result': 'fail'},
                      callback=disconnect_client)
    else:
        socketio.emit('permission', {'result': 'success'})


def send_mail(mail, success, fail):
    curtime_str = datetime.fromtimestamp(
        int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
    uid = mail['scope_uid'][0]

    try:
        res = post(
            message_api,
            headers={'Authorization': 'Token ' + access_token},
            json=mail
        )
        res.raise_for_status()
        success.append({'time': curtime_str, 'uid': uid})
        socketio.emit('send_mails', {'uid': uid, 'status': 'success'})
    except Exception as e:
        fail.append({
            'time': curtime_str,
            'uid': uid,
            'err': str(e)
        })
        socketio.emit('send_mails', {'uid': uid, 'status': 'fail'})


def record_result(success, fail):
    try:
        if len(success) != 0:
            with open('Processed_list.txt', 'a', newline='') as success_file:
                for rec in success:
                    success_file.write(f"[{rec['time']}] {rec['uid']}\n")
        if len(fail) != 0:
            with open('error.log', mode='a', encoding='utf-8') as fail_file:
                for rec in fail:
                    fail_file.write(
                        f"[{rec['time']}] ({rec['uid']}) {rec['err']}\n")
    except Exception as e:
        print(f"[record_result] Error: {str(e)}")


@socketio.on('send_mails')
def handle_mails_sending(mails):
    success = []
    fail = []
    for mail in mails:
        send_mail(mail, success, fail)
    record_result(success, fail)


def sig_app_terminate_handler(sig, frame):
    sleep(5)
    sys.exit(0)


signal.signal(signal.SIGINT, sig_app_terminate_handler)


@app.post('/exitSignal')
def sendSignalToTerminateApp():
    signal.raise_signal(signal.SIGINT)
    return 'success'


if __name__ == '__main__':
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('localhost', 0))
    app_port = temp_socket.getsockname()[1]
    temp_socket.close()
    webbrowser.open_new(f'http://localhost:{app_port}/')
    app.run(host='localhost', port=app_port)
