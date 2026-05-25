import sqlite3
db = sqlite3.connect("TKD - Copy (2).db")
get_student = db.cursor()

student_infos = []
student = get_student.execute("SELECT * FROM STUDENTS WHERE student_id = ?", (s_id,)).fetchall()
    
contactid = get_student.execute("SELECT contact_id FROM STUDENTS_CONTACTS WHERE student_id = ?", (s_id,)).fetchall()
for i in contactid:
    scontact = get_student.execute("SELECT phone, email FROM CONTACTS WHERE contact_id = ?", (i["contact_id"],)).fetchall()
    for t in scontact:
        student_infos.append(tuple(t))
print(student)