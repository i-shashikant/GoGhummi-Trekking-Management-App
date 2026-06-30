import sqlite3
import os
from datetime import datetime


def get_connection():
    conn = sqlite3.connect('trek.db')
    return conn
# def get_connection():
#     print("Using database:", os.path.abspath("trek.db"))

#     conn = sqlite3.connect("trek.db")
#     return conn



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

def get_open_treks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT * FROM treks WHERE status = 'Open'
               """)
    open_treks = cursor.fetchall()

    conn.close()
    return open_treks

def book_trek(user_id, trek_id):
    conn = get_connection()
    cursor = conn.cursor()

    booking_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
               INSERT INTO bookings (user_id, trek_id, booking_date, status)
               VALUES (?, ?, ?, ?)
           """, (user_id, trek_id, booking_date, 'Booked'))

    conn.commit()
    conn.close()

def decrease_available_slots(trek_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               UPDATE treks
               SET available_slots = available_slots - 1
               WHERE id = ?
           """, (trek_id,))

    conn.commit()
    conn.close()

def has_booked_trek(user_id, trek_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT * FROM bookings WHERE user_id = ? AND trek_id = ?
           """, (user_id, trek_id))
    booking = cursor.fetchone()

    conn.close()
    return booking

def get_user_bookings(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT bookings.id, treks.trek_name, treks.location, bookings.booking_date, bookings.status
               FROM bookings
               JOIN treks ON bookings.trek_id = treks.id
               WHERE bookings.user_id = ?
           """, (user_id,))
    bookings = cursor.fetchall()

    conn.close()
    return bookings

# def get_users_by_trek(trek_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT users.id, users.username, users.email
               FROM bookings
               JOIN users ON bookings.user_id = users.id
               WHERE bookings.trek_id = ?
           """, (trek_id,))
    user = cursor.fetchall()

    conn.close()
    return user
