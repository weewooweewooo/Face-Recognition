import mysql.connector
from datetime import datetime
import json
import cv2
import os
from face_utils import FaceUtils
BASE_DIR = r"D:\Git Project\Face-Recognition"

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
            WHERE student_id = %s AND subject_id = %s AND created_at = %s
            """,
            (student_id, subject_id, created_at),
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
            SELECT id, faces FROM admin_system_student
            WHERE enrollment_number = %s
            """,
            (enrollment_number,)
        )
        existing_record = cursor.fetchone()

        if existing_record:
            student_id, existing_faces = existing_record
            if existing_faces:
                existing_faces = json.loads(existing_faces)
                for face_path in existing_faces:
                    full_path = os.path.join(BASE_DIR, face_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        print(f"Deleted old face image: {full_path}")

            cursor.execute(
                """
                UPDATE admin_system_student
                SET name = %s, faculty = %s, faces = %s
                WHERE enrollment_number = %s
                """,
                (name, faculty, json.dumps(file_paths), enrollment_number)
            )
            print("Student record updated successfully.")
        else:
            cursor.execute(
                """
                INSERT INTO admin_system_student (name, enrollment_number, faculty, faces)
                VALUES (%s, %s, %s, %s)
                """,
                (name, enrollment_number, faculty, json.dumps(file_paths))
            )
            print("Student record inserted successfully.")

        conn.commit()
        conn.close()
        
    def load_faces_database(self, subject_id):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE attendance_tracking")
        
        query = """
            SELECT s.id, s.faces 
            FROM admin_system_student AS s
            JOIN admin_system_enrollment AS e ON s.id = e.student_id
            WHERE e.subject_id = %s
        """
        cursor.execute(query, (subject_id,))
        face_data = cursor.fetchall()

        for face in face_data:
            if face['faces']:
                face['faces'] = json.loads(face['faces'])
            else:
                face['faces'] = []

        conn.close()
        return face_data


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'attendance_tracking',
    'port': 3306,
}
