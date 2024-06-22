import os
import datetime
from Evento import Evento

def convertirFecha_Hora(fecha):
    return datetime.datetime.strptime(fecha, '%H:%M')

def getEventos():
    eventos = []
    if os.path.isfile(os.getcwd() + 'eventos.txt'):
        with open('eventos.txt', 'r') as file:
            str_evento = ''
            for l in file:
                if l != '\n':
                    str_evento += l
                else:
                    event = Evento.getEvento(str_evento)
                    eventos.append(event)
                    str_evento = ''
        
        eventos_por_escenario_fecha = {}
        
        for evento in eventos:
            clave = (evento.escenario, evento.fecha)

            if clave not in eventos_por_escenario_fecha:
                eventos_por_escenario_fecha[clave] = []
        
            eventos_por_escenario_fecha[clave].append(evento)

        for lista_eventos in eventos_por_escenario_fecha.items():
            lista_eventos.sort(key=lambda x: x.hora_inicio)
            
        ret = []
        
        for lista_eventos in eventos_por_escenario_fecha:
            ret.append(lista_eventos.values())  # TODO revisar
        
    return eventos

if __name__ == '__main__':
    pass