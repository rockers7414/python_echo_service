import unittest
import uuid
import json
from jsonrpc import JSONRPCResponseManager
from server import dispatcher


class ServerTestCase(unittest.TestCase):

    def test_echo(self):
        request_id = str(uuid.uuid4())
        request = {
            'method': 'echo',
            'params': {'content': 'echo test'},
            'jsonrpc': '2.0',
            'id': request_id
        }

        response = json.loads(JSONRPCResponseManager.handle(json.dumps(request), dispatcher).json)

        self.assertEqual(response['id'], request_id)
        self.assertEqual(response['result'], 'ECHO TEST')

    def test_shutdown(self):
        request_id = str(uuid.uuid4())
        request = {
            'method': 'shutdown',
            'params': {},
            'jsonrpc': '2.0',
            'id': request_id
        }

        response = json.loads(JSONRPCResponseManager.handle(json.dumps(request), dispatcher).json)

        self.assertEqual(response['id'], request_id)
        self.assertEqual(response['result'], 'Server is shutting down...')
