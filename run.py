from flask import Flask

print("Starting...")   # add this temporarily

app = Flask(__name__)

@app.route("/")
def home():
    return "Tutoring Booking System is running!"

if __name__ == "__main__":
    print("Launching Flask...")  # and this
    app.run(debug=True)