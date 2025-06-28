from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

notes = []

@app.route("/addNote", methods=["POST"])
def addNote():
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

    note = {"title": title, "content": content}

    notes.append(note)

    return jsonify({"message": "done"})
