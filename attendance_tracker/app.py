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
    attedance_cards_d ={}
    for i in all:
       acount =db.cursor().execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i["attendance_card_id"],)).fetchall()
       acards.append(tuple(i) + tuple(acount[0]))
    for h in acards:
        card_id = h[3]
        if card_id in attedance_cards_d:
            attedance_cards_d[card_id].append(h)
        else:
            attedance_cards_d[card_id] = [h]
    return render_template("cardpage.html", attedance_cards_d=attedance_cards_d)
@app.route("/edit", methods = ['GET'])            
def edit_page():  
    #userinp = request.form["user_inp"].strip()
    s_id = request.args.get('student_id')
    db = get_db()
    get_student = db.cursor()
    contact_l = []
    sclass = []
    student = get_student.execute("SELECT * FROM STUDENTS WHERE student_id = ?", (s_id,)).fetchall()
    
    contactid = get_student.execute("SELECT contact_id FROM STUDENTS_CONTACTS WHERE student_id = ?", (s_id,)).fetchall()
    classid = get_student.execute("SELECT class_id FROM STUDENTS_CLASSES WHERE student_id = ?", (s_id,)).fetchall()
    for b in classid:
        classday = get_student.execute("SELECT week_day FROM CLASSES WHERE class_id = ?", (b["class_id"],)).fetchall()
        sclass.append(classday[0])
    for i in contactid:
        scontact = get_student.execute("SELECT phone, email FROM CONTACTS WHERE contact_id = ?", (i["contact_id"],)).fetchall()
        for t in scontact:
            contact_l.append((t["phone"], t["email"]))

    return render_template("editpage.html", student=student, sclass=sclass, contact_l=contact_l)

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
