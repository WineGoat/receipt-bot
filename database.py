import sqlite3
from datetime import datetime
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Receipts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT UNIQUE,
        user_id INTEGER,
        amount TEXT,
        date TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Blacklist table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blacklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_id TEXT UNIQUE,
        reason TEXT,
        added_by INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def add_receipt(transaction_id, user_id, amount, date):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO receipts (transaction_id, user_id, amount, date) VALUES (?, ?, ?, ?)",
            (transaction_id, user_id, amount, date)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def is_duplicate(transaction_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM receipts WHERE transaction_id = ?", (transaction_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_to_blacklist(target_id, added_by, reason=""):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO blacklist (target_id, added_by, reason) VALUES (?, ?, ?)",
            (target_id, added_by, reason)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def remove_from_blacklist(target_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blacklist WHERE target_id = ?", (target_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def is_blacklisted(target_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM blacklist WHERE target_id = ?", (target_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM receipts")
    total_receipts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM blacklist")
    total_blacklist = cursor.fetchone()[0]
    conn.close()
    return {
        "total_receipts": total_receipts,
        "total_blacklist": total_blacklist
    }
