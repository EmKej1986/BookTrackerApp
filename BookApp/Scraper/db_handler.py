import sqlite3


class DatabaseConnection:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def get_titles(self):
        query = f'SELECT title FROM Book'
        result = self.con.execute(query).fetchall()
        return result

    def set_is_available(self, book, is_found):
        query = "UPDATE Book SET is_available = ? WHERE title = ?"
        self.con.execute(query, (is_found, book))

    def set_url(self, book, url):
        query = "UPDATE Book Set url = ? WHERE title = ?"
        self.con.execute(query, (url, book))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()
