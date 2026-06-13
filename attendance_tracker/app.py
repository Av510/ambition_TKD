import re #python -m flask --app app run and ctrl c to quit work

from flask import Flask, g, render_template, request, redirect, url_for

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
    attendance_cards_d ={}
    for i in all:
       acount =db.cursor().execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i["attendance_card_id"],)).fetchall()
       acards.append(tuple(i) + tuple(acount[0]))
    for h in acards:
        card_id = h[3]
        if card_id in attendance_cards_d:
            attendance_cards_d[card_id].append(h)
        else:
            attendance_cards_d[card_id] = [h]
    return render_template("cardpage.html", attendance_cards_d=attendance_cards_d)


@app.route("/updateattendance", methods = ['POST'])
def update_attendance():
    change = int(request.form["attendancechange"])
    card_id = request.form["cardid"]
    db = get_db()
    get_update = db.cursor()
    count = get_update.execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (card_id,)).fetchall()
    if count[0]["attendance_count"] == None:
        count = 0
    else:
        count = count[0]["attendance_count"]
    get_update.execute("UPDATE ATTENDANCES SET attendance_count = ? WHERE attendance_card_id = ?", (count, card_id))
    db.commit()
    get_update.execute("UPDATE ATTENDANCES SET attendance_count = attendance_count + ? WHERE attendance_card_id = ?", (change, card_id))
    db.commit()
    return redirect(url_for(("home"), _anchor=card_id))

@app.route("/students")
def student(): 
    db = get_db()
    get_students = db.cursor()
    student_d = {}
    student_infos = get_students.execute("SELECT * FROM STUDENTS ").fetchall()
    for y in student_infos:
        student_class = get_students.execute("SELECT week_day, time FROM STUDENTS_CLASSES LEFT JOIN CLASSES ON STUDENTS_CLASSES.class_id = CLASSES.class_id WHERE student_id= ? ", (y["student_id"],)).fetchall()

        student_contacts = get_students.execute("SELECT CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS LEFT JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE student_id =?", (y["student_id"],)).fetchall()

        student_d[y["student_id"]] = {"Info" : tuple(y) , "Classes" : [tuple(row) for row in student_class] , "Contacts" : [tuple(row) for row in student_contacts]}
    return render_template("studentpage.html", student_d=student_d)

@app.route("/edit", methods = ['GET'] )
def edit_page(): 
    student_d = request.args.get("student_id")
    return render_template("editpage.html", student_d=student_d)
