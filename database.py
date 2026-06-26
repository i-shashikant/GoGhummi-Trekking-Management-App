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
                role TEXT NOT NULL DEFAULT 'user'
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

def add_user(username, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               INSERT INTO users (username, email, password, role)
               VALUES (?, ?, ?, ?)
           """, (username, email, password, role))

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

