import sqlite3
import os


def get_connection():
    conn = sqlite3.connect('trek.db')
    return conn
# def get_connection():
#     print("Using database:", os.path.abspath("trek.db"))

#     conn = sqlite3.connect("trek.db")
#     return conn

def create_tables():
    conn = get_connection() 
    cursor = conn.cursor()

    #Table for User
    cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                approval_status TEXT NOT NULL
            )
               """)
    
    #Tables for treks 
    cursor.execute("""
               CREATE TABLE IF NOT EXISTS treks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trek_name TEXT NOT NULL UNIQUE,
                location TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                duration INTEGER NOT NULL,
                max_slots INTEGER NOT NULL,
                available_slots INTEGER NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                assigned_staff_id INTEGER
            )
               """)

    conn.commit()
    conn.close()
# Treks table indexes:
# 0 = id
# 1 = trek_name
# 2 = location
# 3 = difficulty
# 4 = start_date
# 5 = end_date
# 6 = duration
# 7 = max_slots
# 8 = available_slots
# 9 = description
# 10 = status
# 11 = assigned_staff_id

def add_user(username, email, password, role, approval_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               INSERT INTO users (username, email, password, role, approval_status)
               VALUES (?, ?, ?, ?, ?)
           """, (username, email, password, role, approval_status))

    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT * FROM users WHERE username = ?
           """, (username,))
    user = cursor.fetchone()

    conn.close()
    return user

def add_trek(trek_name, location, difficulty, start_date, end_date,
             duration, max_slots, description, status, assigned_staff_id):
    conn = get_connection()
    cursor = conn.cursor()

    available_slots = max_slots

    cursor.execute("""
               INSERT INTO treks (trek_name, location, difficulty, start_date, end_date,
                                  duration, max_slots, available_slots, description, status, assigned_staff_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           """, (trek_name, location, difficulty, start_date, end_date,
                 duration, max_slots, available_slots, description, status, assigned_staff_id))

    conn.commit()
    conn.close()

def get_all_treks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT * FROM treks
           """)
    treks = cursor.fetchall()

    conn.close()
    return treks

def delete_trek(trek_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               DELETE FROM treks WHERE id = ?
           """, (trek_id,))

    conn.commit()
    conn.close()

def get_trek_by_id(trek_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT * FROM treks WHERE id = ?
           """, (trek_id,))
    trek = cursor.fetchone()

    conn.close()
    return trek

def update_trek(trek_id, trek_name, location, difficulty, start_date, end_date,
                duration, max_slots, description, status, assigned_staff_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               UPDATE treks
               SET trek_name = ?, location = ?, difficulty = ?, start_date = ?, end_date = ?,
                   duration = ?, max_slots = ?, description = ?, status = ?, assigned_staff_id = ?
               WHERE id = ?
           """, (trek_name, location, difficulty, start_date, end_date,
                 duration, max_slots, description, status, assigned_staff_id, trek_id))

    conn.commit()
    conn.close()

def get_pending_staff():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * FROM users WHERE role = 'staff' AND approval_status = 'Pending'
               """)
    pending_staff = cursor.fetchall()

    conn.close()
    return pending_staff


def approve_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   UPDATE users SET approval_status = ? WHERE id = ?
               """, ('Approved', staff_id))

    conn.commit()
    conn.close()

def get_approved_staff():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * FROM users WHERE role = 'staff' AND approval_status = 'Approved'
               """)
    approved_staff = cursor.fetchall()

    conn.close()
    return approved_staff

def get_treks_by_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * from treks WHERE assigned_staff_id = ? 
                   """, (staff_id,))
    treks = cursor.fetchall()
    conn.close
    return treks

def update_trek_by_staff(trek_id, avaialble_slots, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                    UPDATE treks SET available_slots = ?, status = ? WHERE id = ?
                   """,(avaialble_slots, status, trek_id))
    
    conn.commit()
    conn.close()

def update_trek_by_staff(trek_id, available_slots, status):
    conn = get_connection()
    cursor = conn.cursor()  

    cursor.execute("""
                    UPDATE treks
                    SET available_slots = ?, status = ?
                    WHERE id = ?
                   """, (available_slots, status, trek_id))

    conn.commit()
    conn.close()









