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
for a in student_d:
    print(a, student_d[a])