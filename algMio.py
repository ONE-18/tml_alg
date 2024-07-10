import sqlite3
from actuacion import Actuacion
from datetime import datetime, timedelta

# Definir la penalización por cambio de escenario
PENALIZACION_CAMBIO_ESCENARIO = 50

# Eurístico
def calcular_puntuacion(actuacion, tiempo):
    puntuacion = tiempo * actuacion.valor
    return puntuacion

def obtener_artistas(cursor):
    cursor.execute("SELECT * FROM Artista")
    return cursor.fetchall()

def crear_mejor_horario_v1(eventos):
    # Ordenar eventos por hora de fin
    eventos.sort(key=lambda x: x.horafin)
    
    # Programación dinámica para encontrar el mejor horario
    n = len(eventos)
    dp = [0] * (n + 1)
    seleccion = [-1] * (n + 1)
    
    for i in range(1, n + 1):
        incl_puntuacion = calcular_puntuacion(eventos[i-1])
        excl_puntuacion = dp[i-1]
        
        # Encontrar el evento no conflictivo más cercano
        j = i - 1
        while j > 0 and eventos[j-1].horafin > eventos[i-1].horainicio:
            j -= 1
        
        if j > 0:
            incl_puntuacion += dp[j]
        
        if incl_puntuacion > excl_puntuacion:
            dp[i] = incl_puntuacion
            seleccion[i] = j
        else:
            dp[i] = excl_puntuacion
            seleccion[i] = seleccion[i-1]
    
    # Reconstruir el mejor horario
    mejor_horario = []
    i = n
    while i > 0:
        if seleccion[i] != seleccion[i-1]:
            mejor_horario.append(eventos[i-1])
            i = seleccion[i]
        else:
            i -= 1
    
    mejor_horario.reverse()
    return mejor_horario

def crear_mejor_horario_v2(eventos):
    # Ordenar eventos por hora de inicio
    eventos.sort(key=lambda x: x.horainicio)
    
    # Programación dinámica para encontrar el mejor horario
    n = len(eventos)
    dp = [0] * (n + 1)
    seleccion = [-1] * (n + 1)
    tiempo_fin = [0] * (n + 1)
    escenario_actual = [None] * (n + 1)
    
    for i in range(1, n + 1):
        # Puntuación si no se incluye el evento i
        excl_puntuacion = dp[i-1]
        
        # Puntuación si se incluye el evento i (considerando cortar la actuación)
        mejor_incl_puntuacion = 0
        mejor_corte = None
        mejor_escenario = None
        
        for j in range(i):
            if j == 0 or eventos[j-1].horafin <= eventos[i-1].horainicio:
                duracion = (eventos[i-1].horafin - eventos[i-1].horainicio).total_seconds() / 60
                incl_puntuacion = dp[j] + calcular_puntuacion(eventos[i-1], duracion)
                
                # Aplicar penalización si hay un cambio de escenario
                if j > 0 and escenario_actual[j] != eventos[i-1].escenario:
                    incl_puntuacion -= PENALIZACION_CAMBIO_ESCENARIO
                    
                if incl_puntuacion > mejor_incl_puntuacion:
                    mejor_incl_puntuacion = incl_puntuacion
                    mejor_corte = None
                    mejor_escenario = eventos[i-1].escenario
            else:
                duracion = (eventos[j-1].horafin - eventos[i-1].horainicio).total_seconds() / 60
                if duracion > 0:
                    incl_puntuacion = dp[j] + calcular_puntuacion(eventos[i-1], duracion)
                    
                    # Aplicar penalización si hay un cambio de escenario
                    if escenario_actual[j] != eventos[i-1].escenario:
                        incl_puntuacion -= PENALIZACION_CAMBIO_ESCENARIO
                        
                    if incl_puntuacion > mejor_incl_puntuacion:
                        mejor_incl_puntuacion = incl_puntuacion
                        mejor_corte = j
        
        # Decidir si incluir el evento i o no
        if mejor_incl_puntuacion > excl_puntuacion:
            dp[i] = mejor_incl_puntuacion
            seleccion[i] = mejor_corte if mejor_corte is not None else j
            tiempo_fin[i] = eventos[i-1].horafin if mejor_corte is None else eventos[j-1].horafin
            escenario_actual[i] = mejor_escenario
        else:
            dp[i] = excl_puntuacion
            seleccion[i] = seleccion[i-1]
            tiempo_fin[i] = tiempo_fin[i-1]
            escenario_actual[i] = escenario_actual[i-1]
    
    # Reconstruir el mejor horario
    mejor_horario = []
    i = n
    while i > 0:
        if seleccion[i] != seleccion[i-1]:
            if seleccion[i] is not None:
                mejor_horario.append((eventos[i-1], "Cortar en", tiempo_fin[i]))
            else:
                mejor_horario.append((eventos[i-1], "Completo"))
            i = seleccion[i]
        else:
            i -= 1
    
    mejor_horario.reverse()
    return mejor_horario

def valorar_artistas(artistas):
    with open('artistas.txt', 'w', encoding='utf') as f:
        for artista in artistas:
            print(f"{artista[0]}: {artista[1]}")
            f.write(f"{artista[0]}: {artista[1]}\n")
            
    print("Selecciona los artistas que quieres ver (por ID), añade el valor del artista (1 a infinito), con el formato '1-10, 2-24, ...' separados por comas:")
    seleccion = input("IDs de artistas: ")
    seleccionados = seleccion.split(',')
    
    valores_artistas = {}
    
    for s in seleccionados:
        id_artista, valor = s.split('-')
        valor = int(valor.strip())
        # valores_artistas[id_artista.strip()] = int(valor)
        valores_artistas[artistas[int(id_artista.strip())-1][1]] = int(valor)
   
    return valores_artistas

if __name__ == '__main__':
    # Conectar a la base de datos
    conn = sqlite3.connect('bb.db')
    cursor = conn.cursor()

    primer_dia = '2024-07-19'
    eventos = Actuacion.get_eventos_dia(cursor, primer_dia)
    
    artistas = obtener_artistas(cursor)
    valores = valorar_artistas(artistas)
    
    eventos_valorados = Actuacion.asignar_valores(eventos, valores)
    
    mejor_horario = crear_mejor_horario_v2(eventos)
    
    print("\nMejor horario posible:")
    for e in mejor_horario:
        if isinstance(e, tuple):
            print(e[0], e[1])
        else:
            print(e)
    
    conn.close()