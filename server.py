import ctypes
import threading
from jsonrpc import JSONRPCResponseManager, dispatcher


@ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_char_p)
def recv_handler(handler, data):
    request = data.decode('utf-8').strip()
    response = JSONRPCResponseManager.handle(request, dispatcher)
    print('=' * 50)
    print('Request: ' + request)
    echo_server.send_data(handler, response.json.encode('utf-8'))
    print('Response: ' + response.json)
    print('=' * 50)


@dispatcher.add_method
def shutdown():
    echo_server.shutdown()
    return 'Server is shutting down...'


@dispatcher.add_method
def echo(content):
    return content.upper()


echo_server = ctypes.cdll.LoadLibrary('EchoServer.dll')
echo_server.send_data.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
echo_server.reg_recv_handler(recv_handler)


if __name__ == '__main__':
    print('Server initializing...')
    server = threading.Thread(target=echo_server.start)
    server.start()
    server.join()
