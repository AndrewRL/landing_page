from flask import Flask, render_template, jsonify, g, request, flash, redirect, url_for
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route("/_submit_signup_form", methods=["POST"])
def submit_signup_data():
    signup_data = json.loads(request.data)
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()
    data = (datetime.now().timestamp(), signup_data['first_name'], signup_data['last_name'], signup_data['email'])
    cursor.execute("insert into signups values (?, ?, ?, ?)", data)
    return jsonify({"success": True, "message": "Signup form submitted successfully."})

@app.route("/_submit_contact_preferences", methods=["POST"])
def submit_contact_preferences():
    preferences = json.loads(request.data)
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()
    data = (preferences['email'], preferences['notify'], preferences['updates'], preferences['beta'])
    cursor.execute("insert into contact_preferences values (?, ?, ?, ?)", data)

    #Fire confirmation email if user chose a notification option
    if preferences['notify'] or preferences['updates'] or preferences['beta']:
        send_confirmation_email(preferences)

    return jsonify({"success": True, "message": "Signup form submitted successfully."})

def send_confirmation_email(preferences):

    if preferences['beta']:
        #We'll get in touch email
        pass
    elif preferences['updates'] or preferences['notify']:
        #We'll keep you posted / unsubscribe
        pass



if __name__ == '__main__':
    app.run(debug=True)