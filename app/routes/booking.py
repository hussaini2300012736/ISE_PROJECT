from flask import Blueprint, request, jsonify
import sqlite3
from app.tasks import publish_message

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book', methods=['POST'])
def create_booking():
    data = request.json

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # 1. Check tutor exists
    c.execute("SELECT * FROM tutor WHERE id=?", (data['tutor_id'],))
    tutor = c.fetchone()

    if not tutor:
        return {"error": "Tutor not found"}, 404

    # 2. Check availability
    c.execute("""
        SELECT * FROM booking 
        WHERE tutor_id=? AND date=? AND time=?
    """, (data['tutor_id'], data['date'], data['time']))

    existing = c.fetchone()

    if existing:
        return {"error": "Tutor not available"}, 400

    # 3. Create booking
    c.execute("""
        INSERT INTO booking (student_name, tutor_id, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (data['student_name'], data['tutor_id'], data['date'], data['time'], "pending"))

    conn.commit()
    conn.close()

    publish_message('booking_notifications', {
        'student_name': data['student_name'],
        'tutor_id': data['tutor_id'],
        'date': data['date'],
        'time': data['time']
    })

    return {"message": "Booking created"}

@booking_bp.route('/bookings', methods=['GET'])
def get_bookings():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM booking")
    bookings = c.fetchall()

    conn.close()
    return jsonify(bookings)