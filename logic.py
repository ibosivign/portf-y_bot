import sqlite3
from config import DB_NAME


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS portfolio (user_id INTEGER, coin TEXT, amount REAL)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, full_name TEXT, city TEXT, project TEXT)"
    )
    conn.commit()
    conn.close()


def add_asset(user_id: int, coin: str, amount: float):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO portfolio (user_id, coin, amount) VALUES (?, ?, ?)",
        (user_id, coin.upper(), amount),
    )
    conn.commit()
    conn.close()


def get_assets(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT coin, SUM(amount) FROM portfolio WHERE user_id = ? GROUP BY coin",
        (user_id,),
    )
    data = cur.fetchall()
    conn.close()
    return data


def save_user(user_id: int, full_name: str, city: str, project: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (user_id, full_name, city, project) VALUES (?, ?, ?, ?)",
        (user_id, full_name, city, project),
    )
    conn.commit()
    conn.close()


def get_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT full_name, city, project FROM users WHERE user_id = ?",
        (user_id,),
    )
    data = cur.fetchone()
    conn.close()
    return data