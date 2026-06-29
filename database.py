import sqlite3


def get_connection():
    conn = sqlite3.connect('trek.db')
    cursor = conn.cursor()
    return conn

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
                role TEXT NOT NULL
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
                max_slots INTEGER NOT NULL,
                available_slots INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                assigned_staff_id INTEGER
            )
               """)

    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               INSERT INTO users (username, email, password)
               VALUES (?, ?, ?)
           """, (username, email, password))

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