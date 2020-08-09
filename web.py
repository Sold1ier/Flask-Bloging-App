from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>hello</h1>"


@app.route("/<name>")
def user(name):
    return f"hello {name}!"

@app.route("/admin")
def admin():
    return "<h1>ERROR you not an admin</h1>"

if __name__ == "__main__":
    app.run(debug=True)