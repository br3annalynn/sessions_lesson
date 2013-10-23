import sqlite3
from datetime import datetime

# ADMIN_USER="hackbright"
# ADMIN_PASSWORD=5980025637247534551

DB = None
CONN = None

def authenticate(username, hashed_password):
    query = """SELECT id, username, password FROM users where username = ? and password = ?"""
    DB.execute(query, (username, hashed_password))
    row = DB.fetchone()

    if row != None:
        return row[0]
    else:
        return None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def get_user_id_by_username(username):
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    if row != None:
        return row[0]
    else:
        return None

def get_username_by_user_id(user_id):
    query = """SELECT username FROM users WHERE id = ?"""
    DB.execute(query, (user_id,))
    row = DB.fetchone()
    if row != None:
        return row[0]
    else:
        return None

def get_posts_by_user_id(user_id):
    query = """SELECT * FROM user_wall WHERE owner_id = ?"""
    DB.execute(query, (user_id, ))
    rows = DB.fetchall()
    return rows

def insert_post(owner_id, author_id, post_text):
    created_at = datetime.now()
    query = """INSERT into wall_posts (owner_id, author_id, created_at, content) VALUES (?, ?, ?, ?)"""
    DB.execute(query, (owner_id, author_id, created_at, post_text))
    CONN.commit()
    print "***********************************Success!*************************"


