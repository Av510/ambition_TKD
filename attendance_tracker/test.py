import sqlite3
db = sqlite3.connect("TKD.db")

get_all = db.cursor()
all = get_all.execute("SELECT * FROM STUDENTS").fetchall()
acards = []
students = []
share = []
remove = []
ind = []
for i in all:
    acount =db.cursor().execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i[3],)).fetchall()
    acards.append(tuple(i) + tuple(acount[0]))
for t in acards:
    for v in students:
        if t[3] == v[3]: 
            share.append((tuple(t), tuple(v)))
            remove.append(v[3])
            
    students.append(t)

for s in students:
    if s[3] not in remove:
        ind.append(s)
for stu in ind:
    print(stu)
for stud in share:
    print(stud)
