
import sqlite3

class Database:

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # Now that the instance is created, initialize the database
            cls._instance.conn = sqlite3.connect('./data/user_activities.db')
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.cursor.execute("PRAGMA foreign_keys = ON;")  # Enable foreign keys
            cls._instance._create_table()
        return cls._instance

    def _create_table(self):
        """
        Create table(user & entry) if not exist and insert user value as default-data
        """
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date_added DATE NOT NULL DEFAULT CURRENT_DATE,
                            name VARCHAR(20) UNIQUE NOT NULL,
                            weight REAL NOT NULL
                            );""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS entry (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date_added DATE NOT NULL DEFAULT CURRENT_DATE,
                            activity VARCHAR(45) NOT NULL,
                            details VARCHAR(45) NOT NULL,
                            calories REAL NOT NULL DEFAULT 0.0,
                            user_id INTEGER,
                            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
                            );""")

        self.cursor.execute("""
                            INSERT OR IGNORE INTO user (name, weight) VALUES ('Default', 70);
                            """)

        self.conn.commit()


