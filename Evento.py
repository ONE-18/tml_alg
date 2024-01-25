class Evento:
    def __init__(self, artista, fecha, escenario, hora_inicio, hora_fin):
        self.artista = artista
        self.escenario = escenario
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def __str__(self):
        return f"Artista: {self.artista}\nFecha: {self.fecha}\nEscenario: {self.escenario}\nHora inicio: {self.hora_inicio}\nHora fin: {self.hora_fin}\n"