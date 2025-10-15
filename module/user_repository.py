import sqlite3

from module.db import Database

class UserRepository:

    @staticmethod
    def createUser(name, weight) -> bool:
        db = Database()
        try:
            db.cursor.execute("""INSERT INTO user (name, weight) VALUES (?, ?)
                                """, (name, weight))
        except sqlite3.IntegrityError:
            return False
        db.conn.commit()
        return True

    @staticmethod
    def fetch_usernames() -> list:
        conn = Database()
        cursor = conn.cursor
        cursor.execute("SELECT name from user ORDER BY id;")
        # return all first-value in each tuple
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def fetch_user_info(username) -> tuple:
        conn = Database()
        cursor = conn.cursor
        cursor.execute("SELECT id, name, weight from user WHERE name = ?;", (username,))
        # return first result
        return cursor.fetchall()[0]

    @staticmethod
    def deleteUser(user_id):
        db = Database()
        db.cursor.execute("DELETE FROM user WHERE id = ?;", (user_id,))
        db.cursor.execute("DELETE FROM entry where user_id = ?", (user_id,))
        db.conn.commit()