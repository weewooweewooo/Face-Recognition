import mysql.connector
from datetime import datetime
import json
import cv2
import os
from face_utils import FaceUtils

class DatabaseUtils:
    def __init__(self):
        self.db_config = db_config

    def log_attendance(self, created_at, status, student_id, subject_id):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute("USE attendance_tracking")

        cursor.execute(
            """
            SELECT id FROM admin_system_attendance
            WHERE created_at = %s AND student_id = %s AND subject_id = %s
            """,
            (created_at, student_id, subject_id),
        )
        existing_record = cursor.fetchone()

        if existing_record:
            print(
                "Attendance already logged for this student and subject on this date."
            )
        else:
            cursor.execute(
                """
                INSERT INTO admin_system_attendance (created_at, status, student_id, subject_id)
                VALUES (%s, %s, %s, %s)
                """,
                (created_at, status, student_id, subject_id),
            )
            conn.commit()
            print("Attendance logged successfully.")

        conn.close()

    def save_face_to_db(self, name, enrollment_number, faculty, file_paths):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute("USE attendance_tracking")

        cursor.execute(
            """
            INSERT INTO admin_system_student (name, enrollment_number, faculty, faces)
            VALUES (%s, %s, %s, %s)
            """,
            (name, enrollment_number, faculty, json.dumps(file_paths)),
        )

        conn.commit()
        conn.close()
        
    def load_faces_database(self):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE attendance_tracking")

        cursor.execute("SELECT faces FROM admin_system_student")
        face_data = cursor.fetchall()

        for face in face_data:
            face['faces'] = json.loads(face['faces'])

        conn.close()
        return face_data


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'attendance_tracking',
    'port': 3306,
}
