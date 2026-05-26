import sqlite3
db = sqlite3.connect("TKD.db")

get_all = db.cursor()
all = get_all.execute("SELECT * FROM STUDENTS").fetchall()
acards = []
students = []
share = []
remove = []
for i in all:
    acount =db.cursor().execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i[3],)).fetchall()
    acards.append(tuple(i) + tuple(acount[0]))
for t in acards:
    for v in students:
        if t[3] == v[3]: 
            print((tuple(t), tuple(v)))
            share.append((tuple(t), tuple(v)))
            remove.append(t[3])
            
    students.append(t)

