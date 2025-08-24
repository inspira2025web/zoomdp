from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

# Load student data from students.txt
def load_students():
    students = {}
    with open("students.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                index, password = line.split(",")
                students[index.strip()] = password.strip()
    return students

students = load_students()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    index = data.get("indexNumber")
    password = data.get("password")

    if index in students and students[index] == password:
        photo_path = f"photos/{index}.jpg"
        if os.path.exists(photo_path):
            return jsonify({
                "success": True,
                "image": f"/photo/{index}.jpg"
            })
        else:
            return jsonify({
                "success": True,
                "image": None
            })
    else:
        return jsonify({"success": False})

# Serve student photos
@app.route("/photo/<filename>")
def get_photo(filename):
    return send_from_directory("photos", filename)

if __name__ == "__main__":
    app.run(debug=True)
