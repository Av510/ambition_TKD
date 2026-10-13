import sqlite3
db = sqlite3.connect("TKD.db")

db_ex = db.cursor()
attendance_dates = {}
card_d = {}
#acards = db_ex.execute("SELECT STUDENTS.student_id, STUDENTS.first_name, STUDENTS.surname, STUDENTS.card_id, COUNT(ATTENDANCE_RECORDS.attendance_id) FROM STUDENTS LEFT JOIN ATTENDANCE_RECORDS ON STUDENTS.card_id = ATTENDANCE_RECORDS.card_id").fetchall()

#students = db_ex.execute("SELECT * FROM STUDENTS").fetchall()
#for h in students:
 #   card_id = h[3]#card_id
  #  if card_id in card_d:
   #     card_d[card_id]["Students"].append(h[:3])#add h into the list of students for that card_id key
    #else:
#        card_d[card_id] = {"Students": [h[:3]], "Records":[]}#add h as the first value/student in a new list for that (new)card_id key
#arecords = db_ex.execute("SELECT * FROM ATTENDANCE_RECORDS").fetchall()
#for r in arecords:
 #   c_id = r[1]#card_id
  #  if c_id in card_d:         #attendance_id  #date
   #     card_d[c_id]["Records"].append((r[0], r[2]))
sort_c = 1
sort_cards = db.execute("SELECT STUDENTS.* FROM STUDENTS JOIN STUDENTS_CLASSES ON STUDENTS.student_id = STUDENTS_CLASSES.student_id WHERE STUDENTS_CLASSES.class_id = ?", (sort_c,)).fetchall()

print(sort_cards)
