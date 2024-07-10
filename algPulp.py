import pulp
import alg
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('bb.db')
cursor = conn.cursor()

eventos = alg.obtener_actuaciones(cursor)
artistas_preferencias = alg.seleccionar_artistas(alg.obtener_artistas(cursor))

# Crear un problema de optimización
problema = pulp.LpProblem("Horario_Festival", pulp.LpMaximize)

# Variables de decisión
x = pulp.LpVariable.dicts("evento", [e["id"] for e in eventos], cat='Binary')

# Función objetivo: maximizar preferencias
problema += pulp.lpSum([x[e["id"]] * artistas_preferencias[e["artista_id"]] for e in eventos])

# Restricciones para evitar solapamientos
for i in range(len(eventos)):
    for j in range(i + 1, len(eventos)):
        if (eventos[i]["inicio"] < eventos[j]["fin"]) and (eventos[j]["inicio"] < eventos[i]["fin"]):
            problema += x[eventos[i]["id"]] + x[eventos[j]["id"]] <= 1

# Resolver el problema
problema.solve()

# Imprimir el horario óptimo
horario_optimo = [e["id"] for e in eventos if x[e["id"]].varValue == 1]
print("Horario óptimo:", horario_optimo)
