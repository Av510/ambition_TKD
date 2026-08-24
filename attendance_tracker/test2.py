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
  #      print(c + tuple(contactinfo[0]))
        if c[0] in contact_id:
            contact_id[c[0]] += ((c[1], c[2]) + tuple(contactinfo[0]),)
#for a in contact_id:
 #   print(a, contact_id[a])

#for num in student_infos:
   # print(num, student_infos[num])  
  #  print("Contacts:", contact_id[num])
student_infos_list =[]
student_infos = get_students.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname,STUDENTS.attendance_card_id, " \
"CLASSES.week_day, CLASSES.time FROM STUDENTS JOIN STUDENTS_CLASSES ON STUDENTS.student_id = STUDENTS_CLASSES.student_id JOIN CLASSES ON " \
"STUDENTS_CLASSES.class_id = CLASSES.class_id").fetchall()
for y in student_infos:
    scontact = get_students.execute("SELECT CONTACTS.phone, CONTACTS.email, STUDENTS_CONTACTS.relationship_to_student FROM STUDENTS_CONTACTS JOIN CONTACTS ON STUDENTS_CONTACTS.contact_id = CONTACTS.contact_id WHERE student_id =?", (y[0],)).fetchall()
    student_infos_list.append((tuple(y) + (scontact,)))
 #   scday = get_students.execute("SELECT week_day FROM CLASSES WHERE class_id =?", (y[5],)).fetchall()
#    print(scday)
for l in student_infos_list:
    print()
    print(l[:6])
    print("Contacts: ")
    for o in l[6]:
        print(o)  
