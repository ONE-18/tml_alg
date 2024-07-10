import alg
import sqlite3
import pulp
from datetime import datetime, timedelta

# Conectar a la base de datos
conn = sqlite3.connect('bb.db')
cursor = conn.cursor()

actuaciones = alg.obtener_actuaciones(cursor)
artistas_preferidos = alg.seleccionar_artistas(alg.obtener_artistas(cursor))


# Convertir las horas de inicio y fin a objetos datetime y calcular la duración
actuaciones_procesadas = []
for actuacion in actuaciones:
    inicio = datetime.strptime(actuacion[2], "%Y-%m-%d %H:%M")
    fin = datetime.strptime(actuacion[3], "%Y-%m-%d %H:%M")
    duracion = (fin - inicio).total_seconds() / 60  # Duración en minutos
    actuaciones_procesadas.append((actuacion[0], actuacion[1], inicio, fin, duracion))

# Crear el problema de optimización
prob = pulp.LpProblem("Maximizar_Asistencia", pulp.LpMaximize)

# Variables de decisión
x = pulp.LpVariable.dicts("asistir", [actuacion[0] for actuacion in actuaciones_procesadas], cat="Binary")

# Función objetivo: maximizar el tiempo de asistencia a los eventos de artistas preferidos
prob += pulp.lpSum([x[actuacion[0]] * actuacion[4] for actuacion in actuaciones_procesadas if actuacion[1] in artistas_preferidos])

# Restricciones: no se puede asistir a dos actuaciones que se superpongan en el tiempo
for i in range(len(actuaciones_procesadas)):
    for j in range(i + 1, len(actuaciones_procesadas)):
        if actuaciones_procesadas[i][2] < actuaciones_procesadas[j][3] and actuaciones_procesadas[j][2] < actuaciones_procesadas[i][3]:
            prob += x[actuaciones_procesadas[i][0]] + x[actuaciones_procesadas[j][0]] <= 1

# Resolver el problema
prob.solve()

# Resultados
for actuacion in actuaciones_procesadas:
    if pulp.value(x[actuacion[0]]) == 1:
        print(f"Asistir a la actuación {actuacion[0]} del artista {actuacion[1]} de {actuacion[2]} a {actuacion[3]} por {actuacion[4]} minutos")