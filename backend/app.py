from flask import Flask, render_template, request
from flask_cors import cross_origin
import socket
import os
import sys
import webbrowser
import time
from datetime import datetime
from requests import post
import json
import re
import signal


def sig_app_terminate_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, sig_app_terminate_handler)

base_dir = '.'
template_dir = '../frontend/dist/spa'
static_dir = '../frontend/dist/spa/assets'
access_token = None

if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)
    front_dir = os.path.join(base_dir, 'spa')
    template_dir = front_dir
    static_dir = os.path.join(front_dir, 'assets')

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


def get_token():
    token = None
    res = post(
        app.config['TOKEN_URL'],
        data={'username': app.config['ADMIN'],
              'password': app.config['PASSWORD']},
        timeout=5
    )
    if res.status_code == 200:
        result = json.loads(res.text)
        token = result['access_token']
    return token


@app.route('/')
def get_frontpage():
    global access_token
    if access_token is None:
        access_token = get_token()
    return render_template('index.html')


@app.route('/msg', methods=['POST'])
@cross_origin()
def send_req():
    msg_info = request.json
    curtime_str = datetime.fromtimestamp(
        int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

    try:
        msg_info['scope_uid'][0] = re.sub(
            r"[^A-Za-z0-9]+", '', msg_info['scope_uid'][0])
        res = post(
            app.config['MESSAGE_URL'],
            headers={'Authorization': 'Token ' + access_token},
            json=msg_info,
        )
        if res.status_code == 200:
            with open('Processed_list.txt', 'a', newline='') as success_file:
                success_file.write(
                    f"[{curtime_str}] {msg_info['scope_uid'][0]}\n")
            return 'success'
        else:
            raise Exception('Request is failed!')
    except Exception as e:
        with open('error.log', mode='a', encoding='utf-8') as fail_file:
            fail_file.write(
                f"[{curtime_str}] ({msg_info['scope_uid'][0]}) {str(e)}\n")
    return 'fail'


@app.route('/exitSignal', methods=['POST'])
@cross_origin()
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
