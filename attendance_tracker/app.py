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
    student_id = request.args.get("student_id")
    db = get_db()
    at_d = {}
    
    student = db.execute("SELECT * FROM STUDENTS WHERE student_id = ?", (student_id,)).fetchone()
  

    attendance_cards = db.execute("SELECT STUDENTS.first_name, STUDENTS.surname, ATTENDANCES.attendance_card_id, ATTENDANCES.attendance_count FROM ATTENDANCES JOIN STUDENTS ON ATTENDANCES.attendance_card_id = STUDENTS.attendance_card_id").fetchall()
    
    for i in attendance_cards:
        acard_id = i[2]
        if acard_id in at_d:
            at_d[acard_id].append(tuple(i))
        else:
            at_d[acard_id] = [tuple(i)]


    contacts = db.execute("SELECT CONTACTS.contact_id, CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE STUDENTS_CONTACTS.student_id = ?", (student_id,)).fetchall()
    
    classes = db.execute("SELECT * FROM CLASSES").fetchall()
    student_classes = db.execute("SELECT class_id FROM STUDENTS_CLASSES WHERE student_id = ?", (student_id,)).fetchall()
    
    return render_template("editpage.html", student_id=student_id, student_classes=[row["class_id"] for row in student_classes], student=tuple(student), classes=[tuple(row) for row in classes], contacts=[tuple(row) for row in contacts], at_d=at_d)






@app.route("/updatestudent/<student_id>", methods = ['POST'] )
def update_student(student_id): 
#STUDENT INFO
    db = get_db()
    which_form = request.form["which_form"]
    if which_form == "update_student":
        first_name = request.form["first_name"]
        surname = request.form["surname"]
        card_id = request.form["attendance_card_id"]
    
        
        check_card = db.execute("SELECT attendance_card_id FROM ATTENDANCES WHERE attendance_card_id = ?", (card_id,)).fetchone()
        if not check_card:
            db.execute("INSERT INTO ATTENDANCES VALUES (?, 0)", (card_id,))
            db.commit()

        db.execute("UPDATE STUDENTS SET first_name = ?, surname = ?, attendance_card_id = ? WHERE student_id = ?", (first_name, surname, card_id, student_id))
        db.commit()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#CONTACTS
    #delete
    elif which_form == "delete_contact":
        contact_id = request.form["contact_id"]

        db.execute("DELETE FROM STUDENTS_CONTACTS WHERE contact_id = ? AND student_id = ?", (contact_id, student_id))
        db.commit()
    #add
    elif which_form == "add_contact":
        phone = request.form["phone"]
        email = request.form["email"]
        if (phone != "") or (email != ""):
            relationship_to_student = request.form["relationship_to_student"]

            contacts_r = db.execute("INSERT INTO CONTACTS (phone, email) VALUES (?, ?)", (phone, email))
            db.commit()

            contact_id = contacts_r.lastrowid
            db.execute("INSERT INTO STUDENTS_CONTACTS VALUES (?, ?, ?)", (student_id, contact_id, relationship_to_student))
            db.commit()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
    elif which_form == "change_classes":
        db.execute("DELETE FROM STUDENTS_CLASSES WHERE student_id = ?", (student_id,))
        db.commit()
        selected_classes = request.form.getlist("class_ids")
        for cid in selected_classes:
            db.execute("INSERT INTO STUDENTS_CLASSES VALUES (?, ?)", (student_id, cid))
            db.commit()



    return redirect(url_for(("edit_page"), student_id=student_id))
