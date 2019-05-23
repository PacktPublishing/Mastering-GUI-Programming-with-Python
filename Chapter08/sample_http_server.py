from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000


class TestHandler(BaseHTTPRequestHandler):

    def _print_request_data(self):
        print('POST request received')
        print("Content-length: {}".format(self.content_length))
        print(self.data.decode('utf-8'))

    def _send_200(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self, *args, **kwargs):
        self.content_length = self.headers['Content-Length']
        self.data = self.rfile.read(int(self.content_length))
        self._print_request_data()
        self._send_200()
        self.wfile.write('POST successful; received this: \n'.encode('utf-8'))
        self.wfile.write(self.data)


def run(server_class=HTTPServer, handler_class=TestHandler):
    print(f"Launching server at  http://localhost:{PORT}")
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
