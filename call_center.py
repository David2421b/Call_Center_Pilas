import threading
import os
import random


def iniciar():
    mensaje = seleccionar_mensaje()
    print(mensaje)

def seleccionar_mensaje() -> str:
    carpeta = "mensajes"
    lista_txt = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".txt"):
            lista_txt.append(archivo)
    
    if lista_txt:
        archivo_aleatorio = random.choice(lista_txt)
        ruta_completa = os.path.join(carpeta, archivo_aleatorio)
        file = open(ruta_completa, "r", encoding = "utf-8")
        contenido = file.read()
        file.close()
    return contenido


class Agente:
    def __init__(self, id: int, nivel_experiencia: str, estado: str, tiempo_respuesta: int = 0):
        self.id: int = id
        self. nivel_experiencia: str = nivel_experiencia
        self.estado: str = estado
        self.tiempo_respuesta: int = tiempo_respuesta

    def calcular_tiempo(self, longitud_mensaje: int, peso_palabras_calves: int, factor_nivel: float):
        self.tiempo_respuesta = ((longitud_mensaje / 10)+ (peso_palabras_calves / 2) * factor_nivel)


class Queue:
    def __init__(self, priority: str):
        self.queu: list[int] = []
        self.priority: str = priority

    def enqueue(self, e, idx: int = 0):
        if idx == len(self.queu):
            self.queu.append(e)
            return
        if self.priority == "min":
            if e < self.queu[idx]:
                self.queu.insert(idx, e)
                return 
            elif e > self.queu[idx]:
                self.queu.insert(idx + 1, e)
                return
    
        if self.priority == "max":
            if e > self.queu[idx]:
                self.queu.insert(idx, e)
                return 
            elif e < self.queu[idx]:
                self.queu.insert(idx + 1, e)
                return
        return self.enqueue(e, idx + 1)

    def dequeue(self):
        return self.queu.pop(0)
    
    def first(self):
        print(self.queu)
    

class clasificador():
    pass
    

if __name__ == "__main__":
    iniciar()