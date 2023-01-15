# Server Data Managers classes
from SDataManagers.SlinkManager import SlinkManager

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import hashlib

HOST = "0.0.0.0"
HOST_WEB_ACCESS = "127.0.0.1"
WEB_PORT = 4321


class Server(BaseHTTPRequestHandler):  # Web server
    def _set_response(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response(200)

        if self.path != "/":  # short-link redirect request
            short_url = self.path[1:]

            original_url = SlinkManager.get_original_link(short_url)

            if original_url:
                self.wfile.write(bytes(f"<meta http-equiv=\"Refresh\" content=\"0; url=\'{original_url}\'\" />",
                                       "utf-8"))  # redirect
                logging.info(f" [SERVER] Successfully redirected '{short_url}' -> '{original_url}'")

            else:
                logging.info(f" [SERVER] Can't redirect {short_url} -> ?")
                self.wfile.write(bytes(f"<h1>'{short_url}' this short-link doesn't exist</h1>", "utf-8"))

        else:  # index request (no path specified)
            self.wfile.write(bytes("<h1>Welcome to yonka's short-linker!</h1>", "utf-8"))
            self.wfile.write(bytes("<h2>You can use python request to create short-link:</h2>", "utf-8"))

            self.wfile.write(bytes(
                f"<h3>x = requests.post('http://{HOST_WEB_ACCESS}:{WEB_PORT}', "
                f"json={{'url': 'https://long.pasten.com/veryveryverylongurl'}})<br>"
                "print(x.text)</h3>", "utf-8"))

            self.wfile.write(bytes(
                "<h2>If you already got a short-link, "
                f"you can access it via: http://{HOST_WEB_ACCESS}:{WEB_PORT}/short_url</h2>",
                "utf-8"))

    def do_POST(self):
        self._set_response(200)

        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself

        original_url = json.loads(post_data.decode("utf-8"))['url']
        short_url = short_link(original_url.encode())

        # check if shortlink isn't already exist
        already_exist = SlinkManager.is_link_exist(short_url)

        if not already_exist:
            SlinkManager.add_link(short_url, original_url)
            logging.info(f" [SERVER] Successfully saved! ['{original_url}' : '{short_url}']")

        self.wfile.write(f"Short link could be accessed on: {HOST_WEB_ACCESS}:{WEB_PORT}/{short_url}".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=Server):
    logging.basicConfig(level=logging.INFO)
    httpd = server_class((HOST, WEB_PORT), handler_class)

    logging.info(f' [SERVER] Server started on: {HOST_WEB_ACCESS}:{WEB_PORT}')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info(' [SERVER] Stopping server...\n')


def short_link(long_link):
    return str(hashlib.md5(long_link).hexdigest())[-5:]  # take last 5 characters of hashed link (hash with MD5, 128bit)


def main():
    run()


if __name__ == '__main__':
    main()
