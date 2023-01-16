import sqlite3

DB_NAME = "data/links.sqlite"


class DBManager:  # Sqlite management
    @staticmethod
    def get_original_link(short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"SELECT original_url FROM links WHERE short_url = ?", [short_url])
        fetched = cdb.fetchone()

        if fetched:
            original_url = fetched[0]
        else:
            original_url = None

        cdb.close()
        db.close()
        return original_url

    @staticmethod
    def is_link_exist(short_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"SELECT * FROM links WHERE short_url = ?", [short_url])
        fetched = cdb.fetchall()

        if fetched:
            link_exist = fetched[0]
        else:
            link_exist = None

        cdb.close()
        db.close()
        return link_exist

    @staticmethod
    def add_link(short_url, original_url):
        db = sqlite3.connect(DB_NAME)
        cdb = db.cursor()

        cdb.execute(f"INSERT INTO links VALUES (?, ?)", [short_url, original_url])
        db.commit()

        cdb.close()
        db.close()
