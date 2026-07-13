from flask import Flask, jsonify, request
from pymongo import MongoClient
import json

app = Flask(__name__)

# ------------------------
# MongoDB Connection
# ------------------------

client = MongoClient(
    "mongodb://admin:admin123@localhost:27017/?authSource=admin"
)

db = client["todo_db"]
todo_collection = db["todo_items"]

# ------------------------
# Sample student data
# ------------------------

students = []

# ------------------------
# Health Check
# ------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0"
    })

# ------------------------
# Version
# ------------------------

@app.route("/version")
def version():

    return jsonify({
        "version": "1.0.0",
        "environment": "development"
    })

# ------------------------
# Add Student
# ------------------------

@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    student = {
        "id": len(students) + 1,
        "name": data.get("name"),
        "email": data.get("email")
    }

    students.append(student)

    return jsonify({
        "message": "Student added successfully",
        "student": student
    }), 201

# ------------------------
# View Students
# ------------------------

@app.route("/students")
def get_students():

    return jsonify({
        "count": len(students),
        "students": students
    })

# ------------------------
# JSON API
# ------------------------

@app.route("/api")
def api():

    with open("data/students.json", "r") as f:
        data = json.load(f)

    return jsonify(data)

# ==================================================
# TODO API
# ==================================================

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No JSON received"
        }), 400

    todo = {
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription")
    }

    result = todo_collection.insert_one(todo)

    return jsonify({
        "message": "Todo Item Stored Successfully",
        "id": str(result.inserted_id)
    }), 201


@app.route("/submittodoitem", methods=["GET"])
def get_todo_items():

    items = list(
        todo_collection.find(
            {},
            {
                "_id": 0
            }
        )
    )

    return jsonify(items)

# ------------------------
# Home
# ------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "Backend API is running"
    })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
