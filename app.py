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
                id SERIAL PRIMARY KEY,
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

@app.route("/allNotes", methods=["GET"])
def allNotes():

    base = getConnection()
    c = base.cursor()
    c.execute("SELECT title, content FROM notes")
    rows = c.fetchall()
    base.commit()
    base.close()

    notes = []
    for row in rows:
        notes.append({
            "id": row[0],
            "title": row[1],
            "content": row[2]
            })


    return jsonify(notes)