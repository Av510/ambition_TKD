import sqlite3
db = sqlite3.connect("TKD.db")

get_students = db.cursor()
student_infos = {}
contact_id = []
students = get_students.execute("SELECT * FROM STUDENTS").fetchall()
for i in students:
    student_infos[i[0]] = (i[1], i[2], i[3])
    scontact = get_students.execute("SELECT * FROM STUDENTS_CONTACTS WHERE student_id =?", (i[0],)).fetchall()
    for c in scontact:
        contact_id.append(c[0])
    print(i[0])
print(contact_id)
print(student_infos)