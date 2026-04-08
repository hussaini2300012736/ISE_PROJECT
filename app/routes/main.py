from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Tutoring Booking System is running!"