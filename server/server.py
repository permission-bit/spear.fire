from flask import Flask, request

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "secret123"


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == USERNAME and password == PASSWORD:
        return "WELCOME"

    return "Invalid login"


app.run(
    host="127.0.0.1",
    port=5000
)

