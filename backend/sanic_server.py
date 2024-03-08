import multiprocessing
from sanic import Sanic, response
import socketio
import asyncio
import webbrowser
import httpx
import os
import sys
import socket
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

CONCURRENCY_NUM = 10
asyncio_semaphore = asyncio.Semaphore(value=CONCURRENCY_NUM)

app = Sanic(__name__)
sio = socketio.AsyncServer(async_mode='sanic', cors_allowed_origins='*')
sio.attach(app)

base_dir = '../frontend/dist/spa'
template_dir = '../frontend/dist/spa/index.html'
static_dir = '../frontend/dist/spa/assets'

if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)
    template_dir = os.path.join(base_dir, 'index.html')
    static_dir = os.path.join(base_dir, 'assets')

app.static('/assets/', static_dir, name='assets')

token_api = os.getenv('TOKEN_API')
message_api = os.getenv('MESSAGE_API')
admin_info = {
    'username': os.getenv('NAME'),
    'password': os.getenv('PASSWORD'),
}
access_token = None
client_sid = None


@app.get('/')
async def get_app(request):
    global access_token
    try:
        if access_token is None:
            res = httpx.post(token_api, json=admin_info, timeout=5)
            res.raise_for_status()
            access_token = res.json()['access_token']
        return await response.file(template_dir, mime_type='text/html')
    except Exception as e:
        asyncio.create_task(shutdown_server())
        return response.html(body=f"<h3>Internal server Error</h3> \
            <p style='color:red;'>{str(e)}</p>", status=500)


@app.get('/favicon.ico')
async def get_favicon(request):
    return await response.file(os.path.join(base_dir, 'favicon.ico'),
                               mime_type='image/vnd.microsoft.icon')


async def disconnect_client():
    await sio.disconnect(sid=client_sid)


@sio.event
async def connect(sid, environ, auth):
    global client_sid
    client_sid = sid

    if auth['name'] != admin_info['username'] or \
            auth['pwd'] != admin_info['password']:
        await sio.emit('permission', {'result': 'fail'},
                       callback=disconnect_client)
    else:
        await sio.emit('permission', {'result': 'success'})


async def send_mail(client, mail, success, fail):
    async with asyncio_semaphore:
        curtime_str = datetime.fromtimestamp(
            int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
        uid = mail['scope_uid'][0]
        try:
            resp = await client.post(
                message_api,
                headers={'Authorization': 'Token ' + access_token},
                json=mail
            )
            resp.raise_for_status()
            success.append({'time': curtime_str, 'uid': uid})
            await sio.emit('send_mails', {'uid': uid, 'status': 'success'})
        except httpx.HTTPError as e:
            fail.append({
                'time': curtime_str,
                'uid': uid,
                'err': e.response.text
            })
            await sio.emit('send_mails', {'uid': uid, 'status': 'fail'})


def record_result(filename, results):
    with open(filename, 'a') as file:
        for result in results:
            file.write(
                f"[{result['time']}] {result['uid']} \
                    {result['err'] if 'err' in 'result' else ''}\n")


@sio.on('send_mails')
async def handle_mails_sending(_, mails):
    success = []
    fail = []
    try:
        client = httpx.AsyncClient()
        for index in range(0, len(mails), CONCURRENCY_NUM):
            chunk = mails[index:index+CONCURRENCY_NUM]
            tasks = [asyncio.create_task(
                send_mail(client, mail, success, fail)) for mail in chunk]
            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        await client.aclose()
        if len(success) != 0:
            record_result('Processed_list.txt', success)
        if len(fail) != 0:
            record_result('error.log', fail)
    except Exception as e:
        print(e)


async def shutdown_server():
    print("Shutting down server gracefully...")
    await asyncio.sleep(5)
    app.stop()


@app.post('/exitSignal')
async def exit_signal(request):
    asyncio.create_task(shutdown_server())
    return response.text('Server shutdown initiated')

if __name__ == '__main__':
    multiprocessing.freeze_support()
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('127.0.0.1', 0))
    app_port = temp_socket.getsockname()[1]
    temp_socket.close()
    webbrowser.open(f'http://127.0.0.1:{app_port}/')
    app.run(host='127.0.0.1', port=app_port, access_log=False)
