from flask import Flask, render_template, jsonify, g, request, flash, redirect, url_for

app = Flask(__name__)


@app.route("/")
def landing_page():
    return render_template("landing_page.html")

if __name__ == '__main__':
    app.run(debug=True)