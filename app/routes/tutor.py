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

# UPDATE
@tutor_bp.route('/tutors/<int:id>', methods=['PUT'])
def update_tutor(id):
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("UPDATE tutor SET name=?, subject=?, price=? WHERE id=?",
              (data['name'], data['subject'], data['price'], id))

    conn.commit()
    conn.close()
    return {"message": "Tutor updated"}

# DELETE
@tutor_bp.route('/tutors/<int:id>', methods=['DELETE'])
def delete_tutor(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("DELETE FROM tutor WHERE id=?", (id,))

    conn.commit()
    conn.close()
    return {"message": "Tutor deleted"}