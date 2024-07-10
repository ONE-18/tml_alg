import sqlite3
from datetime import datetime

class Actuacion:
    def __init__(self, id, artista, escenario, horainicio, horafin):
        self.id = id
        self.artista = artista
        self.escenario = escenario
        self.horainicio = datetime.strptime(horainicio, "%Y-%m-%d %H:%M")
        self.horafin = datetime.strptime(horafin, "%Y-%m-%d %H:%M")
        self.valor = 1
        
    def __repr__(self):
        return (f"Actuacion(id={self.id}, artista={self.artista}, "
                f"escenario={self.escenario}, horainicio={self.horainicio}, "
                f"horafin={self.horafin})")

    def duracion(self):
        return (self.horafin - self.horainicio).total_seconds() / 60  # Duración en minutos

    @staticmethod
    def get_eventos_dia(cursor, dia):
        cursor.execute("SELECT * FROM Actuación WHERE Horainicio LIKE ?", (f"{dia}%",))
        rows = cursor.fetchall()
        return [Actuacion(*row) for row in rows]