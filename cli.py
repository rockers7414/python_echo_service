import json
import argparse
import socket
import uuid


class RPCClient(object):
    def __init__(self, server, port):
        print('Connect to server({0}:{1})'.format(server, port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))

    def send(self, method, params):
        request = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': str(uuid.uuid4())
        }
        print('Send: '+ json.dumps(request))
        self.sock.sendall((json.dumps(request) + '\n').encode('utf-8'))
        response = self.sock.recv(1024)
        print('Recv: ' + response.decode('utf-8'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command-line interface for ECHO service.')
    subparsers = parser.add_subparsers(help='commands', dest='cmd')
    parser.add_argument('--server', dest='server', default='127.0.0.1', type=str)
    parser.add_argument('--port', dest='port', default=5000, type=int)

    parser_echo = subparsers.add_parser('echo')
    parser_echo.set_defaults(which='echo')
    parser_echo.add_argument('data', help='The data will be sent to server.')

    parser_shutdown = subparsers.add_parser('shutdown')
    parser_shutdown.set_defaults(which='shutdown')

    args = parser.parse_args()

    client = RPCClient(args.server, args.port)
    if args.which == 'echo':
        client.send(args.cmd, {'content': args.data})
    elif args.which == 'shutdown':
        client.send(args.cmd, {})
