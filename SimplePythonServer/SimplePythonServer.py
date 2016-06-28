'''
a simple python server handles POST and GET request and have simple router function

for example, when you come in a request say GET /TestInterface/User/GetUserInfo
you need to write a class in the project folder following the request path
TestInterface.User.GetUserInfo and have a method called do_GET() where you should
return the result for this request in bytes data. The POST request acts the same way
but use do_POST() method.

whatever error, the server will return 404

see the code and the test classes for more detail

'''
import importlib
import http.server
import socketserver
import urllib.parse
import gzip
import cgi
import sys
import os


class Handler(http.server.BaseHTTPRequestHandler):
    def end_with_404(self):
        '''
        whatever exception, return 404
        '''
        self.send_error(404, 'some thing''s wrong, sorry')

    def find_resolver_class(self):
        '''
        automatically find a class base on url, the class should be build in the project folder
        just like the example:TestInterface
        '''
        router_path = urllib.parse.urlparse(self.path).path
        # parse the path to model + class
        # /TestInterface/User/getUserInfo.php -> model:TestInterface.User.GetUserInfo, class:GetUserInfo
        router = os.path.splitext(router_path)[0].lstrip('/')
        # splitext is for cutting like .do(java) .php(PHP)

        if router == '':
            # not handle index
            print('not handle index!')
            return None

        module_name = router.replace('/', '.')
        class_name = str(router.split('/')[-1])

        try:
            return getattr(importlib.import_module(module_name), class_name)
        except ImportError as e:
            # didn't find the class
            print(e)
            return None
        except BaseException as e:
            print(e)
            return None

    def response(self, content):
        '''
        content should be bytes with UTF-8 encoding
        send back the response to client with 200 ok
        '''
        if not type(content) is bytes:
            print('content must be bytes!')
            self.end_with_404()
            return

        self.send_response(200)
        if self.headers['Accept-Encoding'] and 'gzip' in self.headers['Accept-Encoding']:
            # encoding with gzip
            content = gzip.compress(content)
            self.send_header("Content-Encoding", "gzip")

        self.send_header("Content-length", len(content))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        '''
        deal with get request
        '''
        resolver_class = self.find_resolver_class()
        if resolver_class:
            queries = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            res_content = resolver_class().do_GET(queries)
            self.response(res_content)
        else:
            # can't deal with it
            self.end_with_404()

    def do_POST(self):
        '''
        deal with post request
        '''
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            # postvars = cgi.parse_multipart(self.rfile, pdict)
            print('not serve this type right now')
            self.end_with_404()
        elif ctype == 'application/x-www-form-urlencoded':
            # deal with request and get the post body
            length = int(self.headers['content-length'])
            req_content = self.rfile.read(length)
            if pdict['charset']:
                req_content = str(req_content, pdict['charset'].lower())

            resolver_class = self.find_resolver_class()
            if resolver_class:
                # there may be something else in the queries
                queries = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                res_content = resolver_class().do_POST(req_content, queries)
                self.response(res_content)
            else:
                # can't deal with it
                self.end_with_404()
        else:
            print('unsupport ctype')
            self.end_with_404()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':

    ip = 'localhost'
    port = 9000
    server = ThreadedHTTPServer((ip, port), Handler)
    try:
        server.serve_forever()
        sys.stdin.read()
        print('start serving on %s : %s use <Ctrl-C> to stop' % (ip, port))
    except KeyboardInterrupt:
        print('server stop!')
    server.server_close()
