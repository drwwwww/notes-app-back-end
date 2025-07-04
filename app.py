from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import psycopg2

def loadBanned():
    bt = os.getenv("BANNED")
    b = bt.split(",")

    list = []
    for word in b:
        banned_word = word.strip().lower()
        list.append(banned_word)

        return list

banned = loadBanned()

def contains(text):
    text = text.lower()
    for word in banned:
        if word in text:
            return True
    return False

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

    if contains(title) or contains(content):
        return jsonify({"error": "Inappropriate language is not allowed"}), 400

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
    c.execute("SELECT id, title, content FROM notes")
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

    