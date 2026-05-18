import re #python -m flask run and ctrl c to quit work

from flask import Flask, g, render_template, request

import sqlite3

app = Flask(__name__)
DATABASE = "TKD.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def home():  
    db = get_db()
    get_all = db.cursor()
    all = get_all.execute("SELECT * FROM STUDENTS").fetchall()
    acards = []
    for i in all:
       acount =db.cursor().execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i["attendance_card_id"],)).fetchall()
       acards.append(tuple(i) + tuple(acount[0]))

    return render_template("cardpage.html", acards=acards)
