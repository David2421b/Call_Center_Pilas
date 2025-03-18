import threading
import os
import random


def iniciar():
    mensaje = seleccionar_mensaje()
    print(mensaje)
    agente1 = clasificador.crear_agentes()
    agente2 = clasificador.crear_agentes()
    agente3 = clasificador.crear_agentes()
    agente4 = clasificador.crear_agentes()
    print(agente1)
    print(agente2)
    print(agente3)
    print(agente4   )

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
    def __init__(self, id: int, nivel_experiencia: str, estado: str = "Disponible", tiempo_respuesta: int = 0):
        self.id: int = id
        self. nivel_experiencia: str = nivel_experiencia
        self.estado: str = estado
        self.tiempo_respuesta: int = tiempo_respuesta

    def calcular_tiempo(self, longitud_mensaje: int, peso_palabras_calves: int, factor_nivel: float):
        self.tiempo_respuesta = ((longitud_mensaje / 10)+ (peso_palabras_calves / 2) * factor_nivel)
    
    def __repr__(self):
        return f"Mi id es: {self.id} y soy {self.nivel_experiencia}"


class Queue:
    def __init__(self):
        self.queu: list[int] = []

    def enqueue(self, e, idx: int = 0):
        if idx == len(self.queu):
            self.queu.append(e)
            return        
        if e > self.queu[idx]:
            self.queu.insert(idx, e)
            return
        return self.enqueue(e, idx + 1)

    def dequeue(self):
        return self.queu.pop(0)
    
    def __len__(self):
        return len(self.queu)

    def first(self):
        print(self.queu)
    

class clasificador():
    def crear_agentes():
        tipo_experiencias = ["Experto", "Intermedio", "Basico"]
        id = random.randint(1000, 9999)
        experiencia = random.randint(0, len(tipo_experiencias) - 1)
        agente = Agente(id, tipo_experiencias[experiencia])
        return agente
    
    def atender(queue: Queue, agente: Agente):
        "Aca usar los hilos"
        pass



if __name__ == "__main__":
    iniciar()