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
        contacts = get_students.execute("SELECT phone, email FROM CONTACTS WHERE contact_id =?", (c[1],)).fetchall()
        contact_id.append(tuple(c) + tuple(contacts[0]))

for a in contact_id:
    print(a)
    if a[0] in student_infos:
        student_infos[a[0]] += ((a),) #try to do something like all += all except a[0]
for t in student_infos:
    print(t, student_infos[t])
#too difficult to display many contact in one row, so make more details page + avoid cluttering or another format
