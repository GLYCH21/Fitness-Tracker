
from module.db import Database

class EntryRepository:

    @staticmethod
    def add_entry(activity, details, calories, user_id) -> int:
        db = Database()
        db.cursor.execute("""
                          INSERT INTO entry(activity, details, calories, user_id)
                          VALUES (?, ?, ?, ?)
                          """, (activity, details, calories, user_id))
        db.conn.commit()
        return db.cursor.lastrowid

    @staticmethod
    def fetch_entries() -> list[tuple]:
        db = Database()
        db.cursor.execute("SELECT id, date_added, activity, details, calories FROM entry;")
        return db.cursor.fetchall()

    @staticmethod
    def fetch_user_entries(user_id) -> tuple:
        db = Database()
        db.cursor.execute("SELECT id, date_added, activity, details, calories FROM entry WHERE user_id = ?;", (user_id,))
        return db.cursor.fetchall()

    @staticmethod
    def fetch_user_total_burnt_calories(user_id) -> list:
        db = Database()
        db.cursor.execute("SELECT SUM(calories) from entry WHERE user_id = ? and date_added = CURRENT_DATE;", (user_id,))
        return [row[0] for row in db.cursor.fetchall()]

    @staticmethod
    def update_entry(activity, details, calories, entry_id):
        db = Database()
        db.cursor.execute("""UPDATE entry
                        SET activity = ?, details  = ?, calories = ? 
                        WHERE id = ?;
                        """, (activity, details, calories, entry_id))
        db.conn.commit()

    @staticmethod
    def delete_entry(entry_id: int):
        db = Database()
        db.cursor.execute("DELETE FROM entry WHERE id = ?", (entry_id,))
        db.conn.commit()



