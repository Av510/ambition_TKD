import sqlite3
db = sqlite3.connect("TKD - Copy (2).db")
cursor = db.cursor()

all = cursor.execute("SELECT * FROM STUDENTS").fetchall()
for i in all:
    print(i[3])
    acount =cursor.execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i[3],)).fetchall()
    print(tuple(i) + acount[0])