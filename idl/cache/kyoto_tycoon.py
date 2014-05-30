import time
import socket
import urllib
import httplib
import contextlib

from flask import g

from idl import app, json
from idl.cache.base import BaseCache

class KyotoTycoonException(Exception):
    def __init__(self, code, body):
        Exception.__init__(
            self, 'KyotoTycoonException (%d):\n\n%s\n' % (code, body)
        )
        self.code = code
        self.body = body

class KyotoTycoonCache(BaseCache):

    def generate_key(self, *args):
        key = BaseCache.generate_key(self, *args)
        prefix = app.config.get('KYOTO_TYCOON_PREFIX', None)
        if prefix:
            return '.'.join((prefix, key))
        return key

    def test(self):
        try:
            self._send_request('GET', '/', connection=self.get_connection())
        except KyotoTycoonException, e:
            pass

    def get_connection(self):
        return httplib.HTTPConnection(
            app.config['KYOTO_TYCOON_ADDRESS'],
            app.config['KYOTO_TYCOON_PORT'],
            False,
            app.config['KYOTO_TYCOON_TIMEOUT']
        )

    def get(self, key):
        if self.disabled:
            return
        try:
            url = self._get_url(self._encode_args(key))
            data = self._send_request('GET', url, expected_status=200)
            return json.loads(data)
        except KyotoTycoonException, e:
            if e.code == 404:
                return None
            raise

    def set(self, key, value, xt=None):
        if self.disabled:
            return
        key, value = self._encode_args(key, json.dumps(value))
        url = self._get_url(key)
        headers = {}
        if xt != None:
            xt = int(time.time()) + xt
            headers['X-Kt-Xt'] = str(xt)
        self._send_request('PUT', url, value, headers, 201)

    def delete(self, key):
        if self.disabled:
            return
        url = self._get_url(self._encode_args(key))
        headers = {}
        try:
            self._send_request('DELETE', url, expected_status=204)
        except KyotoTycoonException, e:
            ###
            # [CG] Trying to delete something that isn't there isn't really an
            #      error.
            ###
            if e.code != 404:
                raise

    def _encode_args(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                return args[0].encode('utf-8')
            return args[0]
        out = []
        for arg in args:
            if isinstance(arg, str):
                out.append(arg.encode('utf-8'))
            else:
                out.append(arg)
        return out

    def _get_url(self, key):
        return '/' + urllib.quote(key)

    def _check_response_status(self, response, expected_status):
        if response.status != expected_status:
            raise KyotoTycoonException(response.status, response.read())
        return response.read()

    def _send_request(self, method, url, data=None, headers=None,
                            expected_status=200, connection=None):
        conn = connection or g.cache_connection
        conn.request(method, url, data, headers or {})
        response = conn.getresponse()
        data = self._check_response_status(response, expected_status)
        return data

