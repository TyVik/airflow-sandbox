import http.server
import socketserver
from http import HTTPStatus

PORT = 3333


class DemoServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        args = self.path.split('?')[1]
        if args == 'user=tyvik':
            self.send_response(HTTPStatus.OK)
            self.end_headers()
        else:
            self.send_response(HTTPStatus.FORBIDDEN)
            self.end_headers()


with socketserver.TCPServer(("", PORT), DemoServer) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
