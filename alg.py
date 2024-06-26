import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('bb.db')
cursor = conn.cursor()

def obtener_artistas(cursor):
    cursor.execute("SELECT * FROM Artista")
    return cursor.fetchall()

def obtener_actuaciones(cursor):
    cursor.execute("SELECT Artista, Escenario, HoraInicio, HoraFin FROM Actuación")
    return cursor.fetchall()

def obtener_escenarios(cursor):
    cursor.execute("SELECT id, Nombre, Localización FROM Escenario")
    return cursor.fetchall()

def seleccionar_artistas(artistas):
    with open('artistas.txt', 'w', encoding='utf') as f:
        for artista in artistas:
            print(f"{artista[0]}: {artista[1]}")
            f.write(f"{artista[0]}: {artista[1]}\n")
            
    print("Selecciona los artistas que quieres ver (por ID), separados por comas:")
    seleccion = input("IDs de artistas: ")
    seleccionados = seleccion.split(',')
    prioridades = {}
    
    for id_artista in seleccionados:
        prioridad = int(input(f"Prioridad para {artistas[int(id_artista) - 1][1]} (1=Alta, 2=Media, 3=Baja): "))
        prioridades[int(id_artista)] = prioridad
        
    return prioridades

def generar_horario(prioridades, actuaciones):
    actuaciones_filtradas = [act for act in actuaciones if act[0] in prioridades]
    
    # Ordenar actuaciones por prioridad y hora de inicio
    actuaciones_ordenadas = sorted(actuaciones_filtradas, key=lambda x: (prioridades[x[0]], x[2]))
    
    # Crear horario
    horario = []
    for act in actuaciones_ordenadas:
        horario.append({
            'Artista': act[0],
            'Escenario': act[1],
            'HoraInicio': act[2],
            'HoraFin': act[3]
        })
    
    return horario

if __name__ == "__main__":
    artistas = obtener_artistas(cursor)
    actuaciones = obtener_actuaciones(cursor)
    escenarios = obtener_escenarios(cursor)
    
    prioridades = seleccionar_artistas(artistas)
    horario = generar_horario(prioridades, actuaciones)
    
    print("\nHorario Generado:")
    for evento in horario:
        print(f"Artista: {evento['Artista']}, Escenario: {evento['Escenario']}, Hora: {evento['HoraInicio']} - {evento['HoraFin']}")
