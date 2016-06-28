"""
simple client for test
"""

import urllib.request
import urllib.parse
import urllib.error
import threading
import zlib


class HttpClient(object):
    def __init__(self, url, params=None, data=None, header=None):
        self._url = url
        self._params = params
        self._data = data
        self._header = header

    def get(self):
        if self._url:
            url = self._url
            if self._params:
                params = urllib.parse.urlencode(self._params)
                url = (url + "?%s") % params
            request = urllib.request.Request(url)
            if self._header:
                for k in self._header:
                    request.add_header(k, self._header[k])
            request.add_header('Accept-Encoding', 'gzip')

            try:
                response = urllib.request.urlopen(request).read()
            except urllib.error.HTTPError as e:
                print(e)
                return
            decompressed_data = zlib.decompress(response, 16 + zlib.MAX_WBITS)
            print(str(decompressed_data, 'utf-8'))
        else:
            print('url is null')

    def post(self):
        if self._url:
            url = self._url
            if self._params:
                params = urllib.parse.urlencode(self._params)
                url = (url + "?%s") % params
            request = urllib.request.Request(url)
            if self._header:
                for k in self._header:
                    request.add_header(k, self._header[k])
            request.add_header('Accept-Encoding', 'gzip')
            request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            if self._data:
                data = self._data
                data = bytes(data, 'utf-8')
                # request.add_header('Content-Length', len(data))
            else:
                # request.add_header('Content-Length', 0)
                data = bytes('', 'utf-8')

            try:
                response = urllib.request.urlopen(request, data).read()
            except urllib.error.HTTPError as e:
                print(e)
                return
            decompressed_data = zlib.decompress(response, 16 + zlib.MAX_WBITS)
            print(str(decompressed_data, 'utf-8'))
        else:
            print('url is null')


if __name__ == "__main__":

    # target handler is TestRootClass's do_GET method
    def make_get_in_root():
        # with queries and custom header
        HttpClient('http://localhost:9000/TestRootClass.do',
                   {'get_param1': 'a', 'get_param2': 2}, None, {'User-Agent': 'TestClient'}).get()
        # without queries and custom header
        HttpClient('http://localhost:9000/TestRootClass.do', None, None, None).get()

    # target handler is TestRootClass's do_POST method
    def make_post_in_root():
        # with queries and data and custom header
        HttpClient('http://localhost:9000/TestRootClass.do',
                   {'post_param1': 'a', 'post_param2': 2}, 'post data',{'User-Agent': 'TestClient'}).post()
        # without queries and data and custom header
        HttpClient('http://localhost:9000/TestRootClass.do', None, None, None).post()


    # target handler is Interface.User.GetUserInfo's do_GET method
    def make_get_in_user_model():
        # with queries and custom header
        HttpClient('http://localhost:9000/TestInterface/User/GetUserInfo.do',
                   {'get_name': 'bob', 'get_age': 20}, None, {'User-Agent': 'TestClient'}).get()
        # without queries and custom header
        HttpClient('http://localhost:9000/TestInterface/User/GetUserInfo', None, None, None).get()

    # target handler is Interface.User.GetUserInfo's do_POST method
    def make_post_in_user_model():
        # with queries and data and custom header
        HttpClient('http://localhost:9000/TestInterface/User/GetUserInfo.do',
                   {'post_name': 'bob', 'post_age': 20}, 'post data for bob',{'User-Agent': 'TestClient'}).post()
        # without queries and data and custom header
        HttpClient('http://localhost:9000/TestInterface/User/GetUserInfo', None, None, None).post()


    threading.Thread(target=make_get_in_root).start()
    threading.Thread(target=make_post_in_root).start()
    threading.Thread(target=make_get_in_user_model).start()
    threading.Thread(target=make_post_in_user_model).start()
