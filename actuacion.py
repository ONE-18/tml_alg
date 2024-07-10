import sqlite3
from datetime import datetime

class Actuacion:
    def __init__(self, id, artista, escenario, horainicio, horafin, valor=1):
        self.id = id
        self.artista = artista
        self.escenario = escenario
        self.horainicio = datetime.strptime(horainicio, "%Y-%m-%d %H:%M")
        self.horafin = datetime.strptime(horafin, "%Y-%m-%d %H:%M")
        self.valor = valor
        
    def __repr__(self):
        return (f"Actuacion(id={self.id}, artista={self.artista}, "
                f"escenario={self.escenario}, horainicio={self.horainicio}, "
                f"horafin={self.horafin}, valor={self.valor})")

    def duracion(self):
        return (self.horafin - self.horainicio).total_seconds() / 60  # Duración en minutos

    @staticmethod
    def get_eventos_dia(cursor, dia):
        cursor.execute("SELECT * FROM Actuación WHERE Horainicio LIKE ?", (f"{dia}%",))
        rows = cursor.fetchall()
        return [Actuacion(*row) for row in rows]
    
    @staticmethod
    def asignar_valores(eventos, valores_artistas):
        for evento in eventos:
            if evento.artista in valores_artistas:
                evento.valor = valores_artistas[evento.artista]
            else:
                evento.valor = 1  # Valor mínimo si no se encuentra el artista en el diccionario
        return eventos
    
    @staticmethod
    def imprimir_valores_artistas(eventos):
        valores_artistas = {}
        for evento in eventos:
            if evento.artista not in valores_artistas:
                valores_artistas[evento.artista] = evento.valor
        for artista, valor in valores_artistas.items():
            print(f"Artista {artista}: Valor {valor}")
            
            
# def obtener_horas_unicas_ordenadas(eventos):
#     horas = set()
#     for evento in eventos:
#         horas.add(evento.horainicio)
#         horas.add(evento.horafin)
#     return sorted(horas)