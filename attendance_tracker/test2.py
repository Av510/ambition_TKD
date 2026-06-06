import sqlite3
db = sqlite3.connect("TKD.db")

get_students = db.cursor()
student_infos = {}
contact_id = {}
students = get_students.execute("SELECT * FROM STUDENTS").fetchall()
for i in students:
    student_infos[i[0]] = (i[1], i[2], i[3])
    contact_id[i[0]] = []
    scontact = get_students.execute("SELECT * FROM STUDENTS_CONTACTS WHERE student_id =?", (i[0],)).fetchall()
    for c in scontact:
        contactinfo = get_students.execute("SELECT phone, email FROM CONTACTS WHERE contact_id =?", (c[1],)).fetchall()
        print(c + tuple(contactinfo[0]))
        if c[0] in contact_id:
            contact_id[c[0]] += ((c[1], c[2]) + tuple(contactinfo[0]),)
for a in contact_id:
    print(a, contact_id[a])

for num in student_infos:
    print(num, student_infos[num])  
    print("Contacts:", contact_id[num])
