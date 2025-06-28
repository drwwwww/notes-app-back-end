from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import psycopg2

def getConnection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def initData():
    try:
        base = getConnection()
        c = base.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        base.commit()
        base.close()
    except Exception as e:
        print("❌ DB init error:", e)

app = Flask(__name__)
initData()
CORS(app)

@app.route("/addNote", methods=["POST"])
def addNote():
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")


    base = getConnection()
    c = base.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    base.commit()
    base.close()

    return jsonify({"message": "done"})
