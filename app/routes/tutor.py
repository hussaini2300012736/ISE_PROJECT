import sqlite3
from flask import Blueprint, request, jsonify

tutor_bp = Blueprint('tutor', __name__)

# CREATE
@tutor_bp.route('/tutors', methods=['POST'])
def create_tutor():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO tutor (name, subject, price) VALUES (?, ?, ?)",
              (data['name'], data['subject'], data['price']))

    conn.commit()
    conn.close()
    return {"message": "Tutor created"}

# READ
@tutor_bp.route('/tutors', methods=['GET'])
def get_tutors():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM tutor")
    tutors = c.fetchall()

    conn.close()
    return jsonify(tutors)