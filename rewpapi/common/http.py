import httplib
import json
import base64
import sys


class Request(object):
    def __init__(self, auth):
        self.auth = auth
        self.endpoint = None

    def _get_host_path(self, url):
        url = url.replace('http://', '')

        if '/' in url:
            host, path = url.split('/', 1)
            path = '/' + path
        else:
            host, path = url, '/'

        return (host, path)

    def _build_request(self):
        host, path = self._get_host_path(self.endpoint)
        headers = {'Accept': '*/*', 'Host': host}
        auth = '%s:%s' % (self.auth['username'], self.auth['password'])
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        headers.update({'Authorization': auth})
        return (host, path, headers)

    def _request_response(self, host, path, method, headers, body={}):
        conn = httplib.HTTPConnection(host)
        conn.request(method, path + "?token=%s" % self.auth['token'], body, headers)
        res = conn.getresponse()
        response = res.read()
        conn.close()
        return response

    def execute(self, method="GET", body={}):
        host, path, headers = self._build_request()
        response = self._request_response(host, path, method, headers, body)
        
        if response == "Authorization Required":
            return None
        
        try:
            return json.loads(response)
        except ValueError:
            return None
