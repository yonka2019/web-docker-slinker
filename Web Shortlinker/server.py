import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import hashlib
import sqlite3

DB_NAME = "data/links.sqlite"
HOST = "0.0.0.0"
HOST_TO_ACCESS = "localhost"
PORT = 4321


class DBManager:
    @staticmethod
    def get_original_link(short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"SELECT original FROM links WHERE short = '{short_url}';")
        original_url = cdb.fetchone()

        cdb.close()
        db.close()
        return original_url

    @staticmethod
    def is_link_exist(short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"SELECT * FROM links WHERE short = '{short_url}';")
        exist = cdb.fetchall()

        cdb.close()
        db.close()
        return exist

    @staticmethod
    def add_link(original_url, short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"INSERT INTO links VALUES ('{short_url}', '{original_url}', 0);")
        db.commit()

        cdb.close()
        db.close()


class Server(BaseHTTPRequestHandler):
    def _set_response(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response(200)

        if self.path != "/":  # short-link redirect request
            short_url = self.path[1:]

            original_url = DBManager.get_original_link(short_url)

            if original_url:
                original_url = original_url[0]  # get original link
                logging.info(f"Successfully redirected '{short_url}' -> '{original_url}'")
                self.wfile.write(bytes(f"<meta http-equiv=\"Refresh\" content=\"0; url=\'{original_url}\'\" />", "utf-8"))  # redirect

            else:
                logging.info(f"Can't redirect {short_url} -> ?")
                self.wfile.write(bytes(f"<h1>'{short_url}' this short-link doesn't exist</h1>", "utf-8"))

        else:  # index request (no path specified)
            self.wfile.write(bytes("<h1>Welcome to yonka's short-linker!</h1>", "utf-8"))
            self.wfile.write(bytes("<h2>You can use python request to create short-link:</h2>", "utf-8"))

            self.wfile.write(bytes(f"<h3>x = requests.post('http://HOST_TO_ACCESS:{PORT}', json={{'url': 'https://long.pasten.com/veryveryverylongurl'}})<br>"
                                   "print(x.text)</h3>", "utf-8"))

            self.wfile.write(bytes(f"<h2>If you already got a short-link, you can access it via: http://HOST_TO_ACCESS:{PORT}/short_url</h2>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself

        original_url = json.loads(post_data.decode("utf-8"))['url']
        short_url = short_link(original_url.encode())

        # check if shortlink isn't already exist
        already_exist = DBManager.is_link_exist(short_url)

        if already_exist:
            logging.info(f"Already exist '{original_url}' : '{short_url}'")

        else:
            DBManager.add_link(original_url, short_url)

            logging.info(f"Successfully saved! '{original_url}' : '{short_url}'")

        self._set_response(200)
        self.wfile.write(f"Short link: HOST_TO_ACCESS:{PORT}/{short_url}".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=Server):
    logging.basicConfig(level=logging.INFO)
    httpd = server_class((HOST, PORT), handler_class)

    logging.info('Starting httpd...\n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info('Stopping httpd...\n')


def short_link(long_link):
    return str(hashlib.md5(long_link).hexdigest())[-5:]  # take last 5 characters of hashed link (hash with MD5, 128bit)


def main():
    run()


if __name__ == '__main__':
    main()
