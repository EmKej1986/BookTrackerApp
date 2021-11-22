import sqlite3


class DatabaseConnection:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def get_titles(self):
        query = f'SELECT title FROM Book'
        result = self.con.execute(query).fetchall()
        return result

    def get_is_available(self, book):
        is_available_status = True
        query = "UPDATE Book SET is_available = ? WHERE title = ?"
        self.con.execute(query, (is_available_status, book))
        self.con.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()
