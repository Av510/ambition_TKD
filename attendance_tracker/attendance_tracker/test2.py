import sqlite3
db = sqlite3.connect("TKD.db")
student_d = {}
get_a = db.cursor()
payment_due = db.execute("SELECT ATTENDANCE_CARDS.card_id FROM ATTENDANCE_CARDS JOIN ATTENDANCE_RECORDS ON " \
    " ATTENDANCE_CARDS.card_id = ATTENDANCE_RECORDS.card_id WHERE ATTENDANCE_RECORDS.attendance_id > COALESCE(ATTENDANCE_CARDS.clear_id, 0) " \
    " GROUP BY ATTENDANCE_CARDS.card_id HAVING COUNT(*) = 10").fetchall()

for row in payment_due:
    card_id = row[0]#card_id

    students = db.execute(" SELECT first_name, surname FROM STUDENTS WHERE card_id = ?", (card_id,)).fetchall()

    student_d[card_id] = []

    for student in students:
        student_d[card_id].append(student[0] + " " + student[1])#first_name + surname

for cards in student_d:
    print(f"Card ID: {cards}, Students: {', '.join(student_d[cards])}")                                                                    