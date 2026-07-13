from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data (later you’ll replace with DB)
students = []

# ------------------------
# Health Check Endpoint
# ------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0"
    }), 200


# ------------------------
# API Version Endpoint
# ------------------------
@app.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": "1.0.0",
        "environment": "development"
    }), 200


# ------------------------
# Create Student (POST)
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
# Get All Students
# ------------------------
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify({
        "count": len(students),
        "students": students
    }), 200


# ------------------------
# Root
# ------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Backend API is running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
