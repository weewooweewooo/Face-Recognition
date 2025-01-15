import sqlite3
import json
import time

class DatabaseUtils:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS attendance (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          status TEXT NOT NULL,
                          timestamp TEXT NOT NULL)'''
        )
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS faces (
                          id TEXT PRIMARY KEY,
                          name TEXT NOT NULL,
                          file_paths TEXT NOT NULL,
                          timestamp TEXT NOT NULL)'''
        )
        conn.commit()
        conn.close()

    def should_log_attendance(self, name, status, current_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp FROM attendance WHERE name = ? AND status = ? ORDER BY timestamp DESC LIMIT 1",
            (name, status),
        )
        last_log = cursor.fetchone()
        conn.close()
        if last_log:
            last_log_time = time.mktime(time.strptime(last_log[0], '%Y-%m-%d %H:%M:%S'))
            if (current_time - last_log_time) < 300:
                return False
        return True

    def log_attendance(self, name, status, current_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (name, status, timestamp) VALUES (?, ?, ?)",
            (name, status, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))),
        )
        conn.commit()
        conn.close()

    def save_face_to_db(self, face_id, name, file_paths):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO faces (id, name, file_paths, timestamp) VALUES (?, ?, ?, ?)",
            (face_id, name, json.dumps(file_paths), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())),
        )
        conn.commit()
        conn.close()
