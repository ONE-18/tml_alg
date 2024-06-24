import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('bb.db')

# Crear un cursor
cur = conn.cursor()

acts = cur.execute('''SELECT * FROM Actuación''').fetchall()

for a in acts:
    hIni = a[3]
    hFin = a[4]

    if hIni.split(' ')[1].split(':'):
        continue