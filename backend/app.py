from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
import os

app = Flask(__name__)


# =========================
# MongoDB Connection
# =========================

client = MongoClient(
    "mongodb://admin:admin123@localhost:27017/?authSource=admin"
)

db = client["todo_db"]

todo_collection = db["todo_items"]


# =========================
# Sample Student Data
# =========================

students = []


# =========================
# Health Check
# =========================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0"
    }), 200



# =========================
# Version
# =========================

@app.route("/version", methods=["GET"])
def version():

    return jsonify({
        "version": "1.0.0",
        "environment": "development"
    }), 200



# =========================
# Students POST
# =========================

@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    student = {

        "id": len(students)+1,
        "name": data.get("name"),
        "email": data.get("email")

    }

    students.append(student)


    return jsonify({

        "message":"Student added successfully",
        "student":student

    }),201



# =========================
# Students GET
# =========================

@app.route("/students", methods=["GET"])
def get_students():

    return jsonify({

        "count":len(students),
        "students":students

    }),200



# =========================
# JSON API Route
# =========================

@app.route("/api", methods=["GET"])
def api():

    try:

        with open("data/students.json","r") as file:

            data=json.load(file)

        return jsonify(data),200


    except Exception as e:

        return jsonify({

            "error":str(e)

        }),500



# =========================
# TODO POST
# =========================

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    data=request.get_json()


    if not data:

        return jsonify({

            "message":"No JSON data received"

        }),400



    todo={

        "itemName": data.get("itemName"),

        "itemDescription": data.get("itemDescription")

    }



    result = todo_collection.insert_one(todo)



    return jsonify({

        "message":"Todo item stored successfully",

        "id":str(result.inserted_id)

    }),201




# =========================
# TODO GET
# =========================

@app.route("/submittodoitem", methods=["GET"])
def get_todo_items():

    todos=list(
        todo_collection.find(
            {},
            {
                "_id":0
            }
        )
    )


    return jsonify(todos),200



# =========================
# Root
# =========================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "message":"Backend API is running"

    })



# =========================
# Run Application
# =========================

if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
