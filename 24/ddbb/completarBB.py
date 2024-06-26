import sqlite3
import pandas as pd

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('bb.db')

# Crear un cursor
cur = conn.cursor()

hMin = '12:00'

def actualizarFechas(acts):
    i = 0
    for a in acts:
        timeIni = pd.to_datetime(a[3])
        timeFin = pd.to_datetime(a[4])

        if timeIni.time() < pd.Timestamp(hMin).time():
            timeIni += pd.Timedelta(days=1)
            i += 1
            # NtimeIni = timeIni + pd.Timedelta(days=1)
            # print(timeIni.strftime('%Y-%m-%d %H:%M') +' -> '+ NtimeIni.strftime('%Y-%m-%d %H:%M'))
        
        if timeFin.time() < pd.Timestamp(hMin).time():
            timeFin += pd.Timedelta(days=1)
            i += 1
            
        cur.execute('''UPDATE Actuación SET HoraInicio = ?, HoraFin = ? WHERE id = ?''', (timeIni.strftime('%Y-%m-%d %H:%M'), timeFin.strftime('%Y-%m-%d %H:%M'), a[0]))
    # print(i, 'fechas actualizadas')

def iniArtistas(acts):
    
    arrayUnico = list(set(a[1] for a in acts))
    arrayUnico = sorted(arrayUnico)
    
    cur.execute('''DELETE FROM Artista''')
    conn.commit()
    for a in arrayUnico:
        cur.execute('''INSERT OR IGNORE INTO Artista (Nombre) VALUES (?)''', (a,))
    
def iniDistancias(escenarios):
    cur.execute('''DELETE FROM Distancia''')
    conn.commit()
    for esc1 in escenarios:
        for esc2 in escenarios:
            if esc1 != esc2:
                cur.execute('''INSERT INTO Distancia (idEsc1, idEsc2, Distancia, Tiempo) VALUES (?, ?, ?, ?)''', (esc1[0], esc2[0], 0, 0))

def completarBB():
    acts = cur.execute('''SELECT * FROM Actuación''').fetchall()
    actualizarFechas(acts)
    iniArtistas(acts)
    escenarios = cur.execute('''SELECT * FROM Escenario''').fetchall()
    iniDistancias(escenarios)
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    completarBB()