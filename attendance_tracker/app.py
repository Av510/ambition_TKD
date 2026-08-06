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

def get_all_classes():
    db =get_db()
    return  db.execute("SELECT * FROM CLASSES").fetchall()
    
#CARD PAGE-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
@app.route("/")
def home():  
    db = get_db()
    attendance_cards_d = {}
    class_options = get_all_classes()
    acards = db.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname, STUDENTS.attendance_card_id, ATTENDANCES.attendance_count FROM STUDENTS JOIN ATTENDANCES ON STUDENTS.attendance_card_id = ATTENDANCES.attendance_card_id").fetchall()
    for h in acards:
        card_id = h[3]
        if card_id in attendance_cards_d:
            attendance_cards_d[card_id].append(h)
        else:
            attendance_cards_d[card_id] = [h]
    return render_template("cardpage.html", attendance_cards_d=attendance_cards_d, class_options=class_options)
    
#SORT CARD-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/sortcards", methods = ['GET'])
def sort_cards():

    db = get_db()
    sort_cards=""
    attendance_cards_d = {}
    
    class_options = get_all_classes()
    sort_az = request.args.get("alphabetical")
    sort_c = request.args.get("by_class")
    
    
    if sort_az == "first_name":
        sort_cards = db.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname, STUDENTS.attendance_card_id, ATTENDANCES.attendance_count FROM STUDENTS JOIN ATTENDANCES ON STUDENTS.attendance_card_id = ATTENDANCES.attendance_card_id ORDER BY STUDENTS.first_name, STUDENTS.surname").fetchall()
            
    if sort_az == "surname":
        sort_cards = db.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname, STUDENTS.attendance_card_id, ATTENDANCES.attendance_count FROM STUDENTS JOIN ATTENDANCES ON STUDENTS.attendance_card_id = ATTENDANCES.attendance_card_id ORDER BY STUDENTS.surname, STUDENTS.first_name").fetchall()
        
    if sort_c:
        sort_cards = db.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname, STUDENTS.attendance_card_id, ATTENDANCES.attendance_count FROM STUDENTS JOIN ATTENDANCES ON STUDENTS.attendance_card_id = ATTENDANCES.attendance_card_id JOIN STUDENTS_CLASSES ON STUDENTS.student_id = STUDENTS_CLASSES.student_id WHERE STUDENTS_CLASSES.class_id = ?", (sort_c,)).fetchall()


    for sc in sort_cards:
            card_id = sc[3]
            if card_id in attendance_cards_d:
                attendance_cards_d[card_id].append(sc)
            else:
                attendance_cards_d[card_id] = [sc]

    return render_template("cardpage.html", class_options=class_options, attendance_cards_d=attendance_cards_d)



#UPDATE ATTENDANCE-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/updateattendance", methods = ['POST'])
def update_attendance():

    change = int(request.form["attendancechange"])
    card_id = request.form["cardid"]
    og_page = request.form["og_page"]

    db = get_db()

    count = db.execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (card_id,)).fetchall()
    
    if count[0]["attendance_count"] == None:
        count = 0
    else:
        count = count[0]["attendance_count"]
    db.execute("UPDATE ATTENDANCES SET attendance_count = ? WHERE attendance_card_id = ?", (count, card_id))
    db.commit()
    db.execute("UPDATE ATTENDANCES SET attendance_count = attendance_count + ? WHERE attendance_card_id = ?", (change, card_id))
    db.commit()
    return redirect(og_page + "#" + card_id)




#STUDENTS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/students")
def student(): 
    db = get_db()
    student_d = {}
    student_infos = db.execute("SELECT * FROM STUDENTS ").fetchall()

    class_options = get_all_classes()

    for y in student_infos:
        student_class = db.execute("SELECT week_day, time FROM STUDENTS_CLASSES LEFT JOIN CLASSES ON STUDENTS_CLASSES.class_id = CLASSES.class_id WHERE student_id= ? ", (y["student_id"],)).fetchall()

        student_contacts = db.execute("SELECT CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS LEFT JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE student_id =?", (y["student_id"],)).fetchall()

        student_d[y["student_id"]] = {"Info" : tuple(y) , "Classes" : [tuple(row) for row in student_class] , "Contacts" : [tuple(row) for row in student_contacts]}

    return render_template("studentpage.html", student_d=student_d, class_options=class_options)




#SORT STUDENTS--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/sortedstudents", methods = ['GET'] )
def sorted_student(): 

    db = get_db()
    student_d = {}
    sort_student=""


    class_options = get_all_classes()
    sort_az = request.args.get("alphabetical")
    sort_c = request.args.get("by_class")


    if sort_az == "first_name":
        sort_student = db.execute("SELECT * FROM STUDENTS ORDER BY first_name, surname").fetchall()
    if sort_az == "surname":
        sort_student = db.execute("SELECT * FROM STUDENTS ORDER BY surname, first_name").fetchall()
    if sort_c:
        sort_student = db.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname, STUDENTS.attendance_card_id FROM STUDENTS LEFT JOIN STUDENTS_CLASSES ON STUDENTS.student_id = STUDENTS_CLASSES.student_id WHERE class_id =?", (sort_c,) ).fetchall()

    for s in sort_student:
        student_class = db.execute("SELECT week_day, time FROM STUDENTS_CLASSES LEFT JOIN CLASSES ON STUDENTS_CLASSES.class_id = CLASSES.class_id WHERE student_id= ? ", (s["student_id"],)).fetchall()

        student_contacts = db.execute("SELECT CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS LEFT JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE student_id =?", (s["student_id"],)).fetchall()

        student_d[s["student_id"]] = {"Info" : tuple(s) , "Classes" : [tuple(row) for row in student_class] , "Contacts" : [tuple(row) for row in student_contacts]}


    return render_template("studentpage.html", student_d=student_d, class_options=class_options)




@app.route("/edit", methods = ['GET'] )
def edit_page():

    student_id = request.args.get("student_id")
    db = get_db()
    at_d = {}

    og_page = request.args.get("og_page")
    
    student = db.execute("SELECT * FROM STUDENTS WHERE student_id = ?", (student_id,)).fetchone()
  
    
    attendance_cards = db.execute("SELECT STUDENTS.first_name, STUDENTS.surname, ATTENDANCES.attendance_card_id, ATTENDANCES.attendance_count FROM ATTENDANCES LEFT JOIN STUDENTS ON ATTENDANCES.attendance_card_id = STUDENTS.attendance_card_id").fetchall()
    
    for i in attendance_cards:
        acard_id = i[2]
        if acard_id in at_d:
            at_d[acard_id].append(tuple(i))
        else:
            at_d[acard_id] = [tuple(i)]


    contacts = db.execute("SELECT CONTACTS.contact_id, CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE STUDENTS_CONTACTS.student_id = ?", (student_id,)).fetchall()
    
    classes = get_all_classes()
    student_classes = db.execute("SELECT class_id FROM STUDENTS_CLASSES WHERE student_id = ?", (student_id,)).fetchall()

    all_contacts = db.execute("SELECT * FROM CONTACTS").fetchall()
    
    return render_template("editpage.html", student_id=student_id, student_classes=[row["class_id"] for row in student_classes], student=tuple(student), classes=[tuple(row) for row in classes], contacts=[tuple(row) for row in contacts], at_d=at_d, all_contacts=all_contacts, og_page=og_page)






@app.route("/updatestudent/<student_id>", methods = ['POST'] )
def update_student(student_id): 
#STUDENT INFO
    db = get_db()
    
    which_form = request.form["which_form"]

    if which_form != "delete_student":
         og_page = request.form["og_page"]

#BASIC STUDENT INFO----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if which_form == "update_student":
        first_name = request.form["first_name"]                     
        surname = request.form["surname"]
        card_id = request.form["attendance_card_id"]
    
        
        check_card = request.form.get("new_card")
        if check_card:
            new_card = db.execute("INSERT INTO ATTENDANCES (attendance_count) VALUES (0)")
            db.commit()
            card_id = new_card.lastrowid


        db.execute("UPDATE STUDENTS SET first_name = ?, surname = ?, attendance_card_id = ? WHERE student_id = ?", (first_name, surname, card_id, student_id))
        db.commit()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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


    elif which_form == "select_contact":
        exist_contact = request.form["exist_contact"]
        relation_ex = request.form["relation_ex"]

        if exist_contact != "":
            db.execute("INSERT INTO STUDENTS_CONTACTS VALUES (?, ?, ?)", (student_id, exist_contact, relation_ex))
            db.commit()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
    elif which_form == "change_classes":
        db.execute("DELETE FROM STUDENTS_CLASSES WHERE student_id = ?", (student_id,))
        db.commit()
        selected_classes = request.form.getlist("class_ids")
        for cid in selected_classes:
            db.execute("INSERT INTO STUDENTS_CLASSES VALUES (?, ?)", (student_id, cid))
            db.commit()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DELETE STUDENT !!!

    elif which_form == "delete_student":
        db.execute("DELETE FROM STUDENTS_CLASSES WHERE student_id = ?", (student_id,))
        
        
        db.execute("DELETE FROM STUDENTS_CONTACTS WHERE student_id = ?", (student_id,))
        

        db.execute("DELETE FROM STUDENTS WHERE student_id = ?", (student_id,))

        db.commit()

        return redirect(url_for("student"))

    return redirect(url_for(("edit_page"), student_id=student_id, og_page=og_page))


#Seacrch student--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/searchstudent", methods=["GET"])
def search_student():

    student = request.args.get("user_search", "").lower().strip()

    db = get_db()
    student_d = {}
    student_infos = db.execute("SELECT * FROM STUDENTS WHERE TRIM(LOWER(first_name)) LIKE ? || '%' OR TRIM(LOWER(surname)) LIKE ? || '%'", (student, student)).fetchall()
    
    class_options = get_all_classes()
    
    for y in student_infos:
        student_class = db.execute("SELECT week_day, time FROM STUDENTS_CLASSES LEFT JOIN CLASSES ON STUDENTS_CLASSES.class_id = CLASSES.class_id WHERE student_id= ? ", (y["student_id"],)).fetchall()
    
        student_contacts = db.execute("SELECT CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS LEFT JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE student_id =?", (y["student_id"],)).fetchall()
    
        student_d[y["student_id"]] = {"Info" : tuple(y) , "Classes" : [tuple(row) for row in student_class] , "Contacts" : [tuple(row) for row in student_contacts]}
    
    return render_template("studentpage.html", student_d=student_d, class_options=class_options)





#New student ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/newstudent")
def add_student():

    db = get_db()
    at_d = {}
  
    og_page = request.args.get("og_page")

    attendance_cards = db.execute("SELECT STUDENTS.first_name, STUDENTS.surname, ATTENDANCES.attendance_card_id, ATTENDANCES.attendance_count FROM ATTENDANCES LEFT JOIN STUDENTS ON ATTENDANCES.attendance_card_id = STUDENTS.attendance_card_id").fetchall()
    
    for i in attendance_cards:
        acard_id = i[2]
        if acard_id in at_d:
            at_d[acard_id].append(tuple(i))
        else:
            at_d[acard_id] = [tuple(i)]

    classes = get_all_classes()

    contacts = db.execute("SELECT * FROM CONTACTS").fetchall()

    return render_template("addstudent.html", at_d=at_d, classes=classes, contacts=[tuple(row) for row in contacts], og_page=og_page)




@app.route("/createstudent", methods=["POST"])
def create_student():
    db = get_db()

    name = request.form["name"]
    surname = request.form["surname"]
    card_id = request.form["attendance_card_id"]

    phone = request.form["phone"]
    email = request.form["email"]
    relation = request.form["relationship_to_student"]
    phone2 = request.form["phone2"]
    email2 = request.form["email2"]
    relation2 = request.form["relationship_to_student2"]
    contact_ex = request.form["existing_contact"]
    relation_ex = request.form["relationship_to_student_ex"]
    contact_ex2 = request.form["existing_contact2"]
    relation_ex2 = request.form["relationship_to_student_ex2"]

    selected_classes = request.form.getlist("class_ids")
#NEW Card---------------------------------------------------------------------------------------------------------------------------------------
    check_card = request.form.get("new_card")
    if check_card:
        new_card = db.execute("INSERT INTO ATTENDANCES (attendance_count) VALUES (0)")
        
        card_id = new_card.lastrowid
#NEW Student-------------------------------------------------------------------------------------------------------------------------------

    new_student = db.execute("INSERT INTO STUDENTS (first_name, surname, attendance_card_id) VALUES (?, ?, ?)", (name, surname, card_id))
    student_id = new_student.lastrowid

#NEW Contact(s)---------------------------------------------------------------------------------------------------------------------------------------
    if (phone.strip() != "") or (email.strip() != ""):

        contacts_r = db.execute("INSERT INTO CONTACTS (phone, email) VALUES (?, ?)", (phone, email))
        

        contact_id = contacts_r.lastrowid
        db.execute("INSERT INTO STUDENTS_CONTACTS VALUES (?, ?, ?)", (student_id, contact_id, relation))
        

    if (phone2.strip() != "") or (email2.strip() != ""):

        contacts_r2 = db.execute("INSERT INTO CONTACTS (phone, email) VALUES (?, ?)", (phone2, email2))

        contact_id2 = contacts_r2.lastrowid
        db.execute("INSERT INTO STUDENTS_CONTACTS VALUES (?, ?, ?)", (student_id, contact_id2, relation2))
    #user select from existing contactts     
    if contact_ex:
        db.execute("INSERT INTO STUDENTS_CONTACTS VALUES (?, ?, ?)", (student_id, contact_ex, relation_ex))

    if contact_ex2:
        db.execute("INSERT INTO STUDENTS_CONTACTS VALUES (?, ?, ?)", (student_id, contact_ex2, relation_ex2))


#Classes----------------------------------------------------------------------------------------------------------------------------------------------
    for cid in selected_classes:
            db.execute("INSERT INTO STUDENTS_CLASSES VALUES (?, ?)", (student_id, cid))

    db.commit()

    return redirect(url_for("student"))
