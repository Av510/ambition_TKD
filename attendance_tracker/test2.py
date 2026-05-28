import sqlite3
db = sqlite3.connect("TKD.db")

get_all = db.cursor()
all = get_all.execute("SELECT * FROM STUDENTS").fetchall()
acards = []
attedance_cards_d = {}
for i in all:
    acount =db.cursor().execute("SELECT attendance_count FROM ATTENDANCES WHERE attendance_card_id = ?", (i[3],)).fetchall()
    acards.append(tuple(i) + tuple(acount[0]))
for h in acards:
    card_id = h[3]
    if card_id in attedance_cards_d:
        attedance_cards_d[card_id].append(h)
    else:
        attedance_cards_d[card_id] = [h]
for v in attedance_cards_d:
    print(v, attedance_cards_d[v])