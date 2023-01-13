import sqlite3

DB_NAME = "data/links.sqlite"


class DBManager:  # Sqlite management
    @staticmethod
    def get_original_link(short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"SELECT original_url FROM links WHERE short_url = '{short_url}';")
        original_url = cdb.fetchone()

        cdb.close()
        db.close()
        return original_url

    @staticmethod
    def is_link_exist(short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"SELECT * FROM links WHERE short_url = '{short_url}';")
        link_exist = cdb.fetchall()

        cdb.close()
        db.close()
        return link_exist

    @staticmethod
    def add_link(short_url, original_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"INSERT INTO links VALUES ('{short_url}', '{original_url}');")
        db.commit()

        cdb.close()
        db.close()
