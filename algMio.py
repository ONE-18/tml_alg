import sqlite3
from actuacion import Actuacion
from datetime import datetime, timedelta

def obtener_horas_unicas_ordenadas(eventos):
    horas = set()
    for evento in eventos:
        horas.add(evento.horainicio)
        horas.add(evento.horafin)
    return sorted(horas)

def calcular_puntuacion(actuacion):
    return actuacion.duracion() * actuacion.valor

def crear_mejor_horario(eventos):
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


if __name__ == '__main__':
    
    # Conectar a la base de datos
    conn = sqlite3.connect('bb.db')
    cursor = conn.cursor()

    primer_dia = '2024-07-19'
    eventos = Actuacion.get_eventos_dia(cursor, primer_dia)
    
    horas_unicas_ordenadas = obtener_horas_unicas_ordenadas(eventos)
    # print("Horas únicas y ordenadas:")
    # for hora in horas_unicas_ordenadas:
    #     print(hora)
    
    mejor_horario = crear_mejor_horario(eventos)
    
    print("Mejor horario posible:")
    for e in mejor_horario:
        print(e)
    
    conn.close()