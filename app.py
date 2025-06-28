from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

def initData():
    base = sqlite3.connect("database.db")
    c = base.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    c.commit()
    c.close()

app = Flask(__name__)
initData()
CORS(app)

@app.route("/addNote", methods=["POST"])
def addNote():
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

    base = sqlite3.connect("database.db")
    c = base.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)" title, content)
    c.commit()
    c.close()
    
    return jsonify({"message": "done"})
