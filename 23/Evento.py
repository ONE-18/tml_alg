class Evento:
    def __init__(self, artista, fecha, escenario, hora_inicio, hora_fin):
        self.artista = artista
        self.escenario = escenario
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
    
    def __init__(self, data):
        if len(data) != 5:
            raise Exception("Error en el formato de los datos")
        self.artista = data[0]
        self.escenario = data[1]
        self.fecha = data[2]
        self.hora_inicio = data[3]
        self.hora_fin = data[4]
    
    def __str__(self):
        return f"Artista-> {self.artista}\nFecha-> {self.fecha}\nEscenario-> {self.escenario}\nHora inicio-> {self.hora_inicio}\nHora fin-> {self.hora_fin}\n"
    
    @staticmethod
    def getEvento(str):
        data = []
        for l in str:
            data.append(l.split('->')[1])
        return Evento(data)
