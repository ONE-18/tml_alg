import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('bb.db')

# Crear un cursor
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Artista''')
cur.execute('''DROP TABLE IF EXISTS Actuación''')
cur.execute('''DROP TABLE IF EXISTS Escenario''')
cur.execute('''DROP TABLE IF EXISTS Distancia''')

# Crear una tabla
cur.execute('''CREATE TABLE IF NOT EXISTS Artista (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(50)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Actuación (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Artista INTEGER,
    Escenario INTEGER,
    HoraInicio DATETIME,
    HoraFin DATETIME,
    FOREIGN KEY (Artista) REFERENCES Artista(id),
    FOREIGN KEY (Escenario) REFERENCES Escenario(id)
)
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Escenario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(50),
    Localización VARCHAR(50)
)
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Distancia (
    idEsc1 INTEGER,
    idEsc2 INTEGER,
    Distnacia FLOAT,
    Tiempo FLOAT,
    FOREIGN KEY (idEsc1) REFERENCES Actuación(id),
    FOREIGN KEY (idEsc2) REFERENCES Escenario(id)
)
''')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
