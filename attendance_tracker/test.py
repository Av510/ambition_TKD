import sqlite3
db = sqlite3.connect("TKD.db")

get_students = db.cursor()
student_d = {}
student_infos = get_students.execute("SELECT * FROM STUDENTS ").fetchall()
for y in student_infos:
    student_class = get_students.execute("SELECT week_day, time FROM STUDENTS_CLASSES LEFT JOIN CLASSES ON STUDENTS_CLASSES.class_id = CLASSES.class_id WHERE student_id= ? ", (y[0],)).fetchall()
    #print(y)
   # print(student_class)
    student_contacts = get_students.execute("SELECT CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS LEFT JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE student_id =?", (y[0],)).fetchall()
   # print(student_contacts)
    s_id = y[0]
    student_d[y[0]] = {"Info" : y , "Class" : student_class , "Contacts" : student_contacts}
#students have multiple or zero contact and class days
card_id = 100
first_name = "Lucas"
surname = "Chew"
student_id = 3
check_card = db.execute("SELECT attendance_card_id FROM ATTENDANCES WHERE attendance_card_id = ?", (card_id,)).fetchone()


if not check_card:
    db.execute("INSERT INTO ATTENDANCES VALUES (?, 0)", (card_id,))
    db.commit()

db.execute("UPDATE STUDENTS SET first_name = ?, surname = ?, attendance_card_id = ? WHERE student_id = ?", (first_name, surname, card_id, student_id))
db.commit()
print(check_card)