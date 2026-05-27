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
