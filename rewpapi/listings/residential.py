import httplib
import json
import base64
import sys


USERNAME = "myusername"
PASSWORD = "mypassword"
TOKEN = "abcd1234-4321-1234-abcd-123456789101"


def request_response(host, path, method, headers, body={}):
    conn = httplib.HTTPConnection(host)
    conn.request(method, path + "?token=%s" % TOKEN, body, headers)
    res = conn.getresponse()
    response = res.read()
    conn.close()
    return response


def get_host_path(url):
    url = url.replace('http://', '')

    if '/' in url:
        host, path = url.split('/', 1)
        path = '/' + path
    else:
        host, path = url, '/'

    return (host, path)


def build_request(url):
    host, path = get_host_path(url)
    headers = {'Accept': '*/*', 'Host': host}
    auth = '%s:%s' % (USERNAME, PASSWORD)
    auth = 'Basic %s' % base64.encodestring(auth)
    auth = auth.strip()
    headers.update({'Authorization': auth})
    return (host, path, headers)


def run(branch_uuid=None):
    url = "http://www.yoursite.co.za/api/branches/"
    if branch_uuid:
        url += "%s/" % branch_uuid
    host, path, headers = build_request(url)
    response = request_response(host, path, "GET", headers)

    if branch_uuid:
        branch = json.loads(response)
        print branch['branch_manager']
    else:
        branches = json.loads(response)
        for branch in branches:
            print branch['branch_name'], branch['uuid']


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[-1])
    else:
        run()
