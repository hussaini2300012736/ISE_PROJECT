import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
import sqlite3

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_bookings(client):
    response = client.get('/bookings')
    assert response.status_code == 200

def test_create_booking_tutor_not_found(client):
    response = client.post('/book', json={
        'student_name': 'Test Student',
        'tutor_id': 9999,
        'date': '2026-05-01',
        'time': '10:00'
    })
    assert response.status_code == 404
    assert b'Tutor not found' in response.data

def test_get_tutors(client):
    response = client.get('/tutors')
    assert response.status_code == 200

def test_payment_offline(client):
    response = client.post('/payment/offline', json={
        'booking_id': 1
    })
    assert response.status_code == 200
    assert b'Offline payment recorded' in response.data

def test_payment_create_missing_data(client):
    response = client.post('/payment/create', json={})
    assert response.status_code == 400