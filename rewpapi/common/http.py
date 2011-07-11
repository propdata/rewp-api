import logging
import httplib
import json
import base64
import sys


class Request(object):
    def __init__(self, auth):
        self._auth = auth
        self._endpoint = None

    def _get_host_path(self, url):
        url = url.replace('http://', '')

        if '/' in url:
            host, path = url.split('/', 1)
            path = '/' + path
        else:
            host, path = url, '/'

        return (host, path)

    def _build_request(self):
        host, path = self._get_host_path(self._endpoint)
        headers = {'Accept': '*/*', 'Host': host}
        auth = '%s:%s' % (self._auth['username'], self._auth['password'])
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        headers.update({'Authorization': auth})
        return (host, path, headers)

    def _request_response(self, host, path, method, headers, body=""):
        if body:
            body = json.dumps(body)
            headers['content-type'] = 'application/json'

        conn = httplib.HTTPConnection(host)
        conn.request(method, path + "?token=%s" % self._auth['token'],
                body, headers)
        res = conn.getresponse()
        response = res.read()
        conn.close()
        return response

    def execute(self, method="GET", body=""):
        host, path, headers = self._build_request()
        response = self._request_response(host, path, method, headers, body)

        if response == "Authorization Required":
            return None

        if response == "Bad Request":
            logging.warning("Bad Request")
        
        try:
            return json.loads(response)
        except ValueError:
            return None
