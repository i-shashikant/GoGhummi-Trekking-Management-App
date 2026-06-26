import sqlite3


def get_connection():
    conn = sqlite3.connect('trek.db')
    cursor = conn.cursor()
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
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