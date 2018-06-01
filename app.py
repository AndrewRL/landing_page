from flask import Flask, render_template, jsonify, g, request, flash, redirect, url_for
import sqlite3
import json
import mailchimp
import os
from datetime import datetime

app = Flask(__name__)
MAILCHIMP_API = os.environ['MAILCHIMP_API']
NOTIFY_LIST_ID = os.environ['NOTIFY_LIST_ID']


@app.route("/")
def landing_page():
    return render_template("landing_page.html")


@app.route("/_submit_signup_form", methods=["POST"])
def submit_signup_data():
    signup_data = json.loads(request.data)
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()
    data = (datetime.now().timestamp(), signup_data['first_name'], signup_data['last_name'], signup_data['email'])
    try:
        cursor.execute("insert into signups values (?, ?, ?, ?)", data)
    except sqlite3.IntegrityError:
        print("{} is already registered.".format(signup_data['email']))
        return jsonify({"success": False, "message": "User already in database."})

    db_conn.commit()
    print(list(cursor.execute("select * from signups")))
    return jsonify({"success": True, "message": "Signup form submitted successfully."})


@app.route("/_submit_contact_preferences", methods=["POST"])
def submit_contact_preferences():
    preferences = json.loads(request.data)
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()
    data = (preferences['email'], preferences['notify'], preferences['updates'], preferences['beta'])
    try:
        cursor.execute("insert into contact_preferences values (?, ?, ?, ?)", data)
    except sqlite3.IntegrityError:
        print("This user's preferences have already been entered.")

    db_conn.commit()

    #Fire confirmation email if user chose a notification option
    if preferences['notify'] or preferences['updates'] or preferences['beta']:
        add_to_email_lists(preferences)

    return jsonify({"success": True, "message": "Signup form submitted successfully."})


def add_to_email_lists(preferences):
    api = mailchimp.Mailchimp(MAILCHIMP_API)
    db_conn = sqlite3.connect("leads.db")
    cursor = db_conn.cursor()
    print(preferences)
    print(list(cursor.execute("select * from signups")))
    user_info = cursor.execute("select * from signups where email=?", (preferences['email'],)).fetchone()

    if preferences['beta']:
        pass

    if preferences['updates']:
        api.lists.subscribe(NOTIFY_LIST_ID, {"email": user_info[3]},
                            merge_vars={"FNAME": user_info[1], "LNAME": user_info[2]})
    elif preferences['notify']:
        api.lists.subscribe(NOTIFY_LIST_ID, {"email": user_info[3]},
                            merge_vars={"FNAME": user_info[1], "LNAME": user_info[2]})


if __name__ == '__main__':
    app.run(debug=True)