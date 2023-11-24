import sqlite3


class DatabaseConnection:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def get_titles(self):
        query = "SELECT title FROM Book"
        result = self.con.execute(query).fetchall()
        return result

    def set_is_available(self, book, is_found):
        query = "UPDATE Book SET is_available = ? WHERE title = ?"
        self.con.execute(query, (is_found, book))

    def set_url(self, book, url):
        query = "UPDATE Book Set url = ? WHERE title = ?"
        self.con.execute(query, (url, book))

    def get_book_by_title(self, selected_title):
        query = "SELECT is_available, id FROM Book WHERE title = ?"
        result = self.con.execute(query, (selected_title,)).fetchone()
        return result

    def get_users_profile_id(self, book_id):
        query = "SELECT UserProfile_id FROM book_identifier WHERE book_id = ? IN (SELECT book_id FROM book_identifier)"
        result = self.con.execute(query, (book_id,)).fetchall()
        return result

    def get_users_email(self, profile_id):
        query = "SELECT email FROM User WHERE user_profile = ?"
        result = self.con.execute(query, (profile_id,)).fetchone()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()
