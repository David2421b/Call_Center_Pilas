import threading
import os
import random


def iniciar():
    agentes = Llamado_Unico.crear_agentes()
    unico = Llamado_Unico()
    unico.agente_disponible(agentes)
    unico_txt = Llamado_Unico()
    mensaje = unico_txt.seleccionar_mensaje()
    print(mensaje)
    

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
    

class Llamado_Unico:
    def crear_agentes() -> list:
        lista_agente = []
        for _ in range(0, 4):
            tipo_experiencias = ["Experto", "Intermedio", "Basico"]
            id = random.randint(1000, 9999)
            experiencia = random.randint(0, len(tipo_experiencias) - 1)
            agente = Agente(id, tipo_experiencias[experiencia])
            lista_agente.append(agente)
        return lista_agente

    def agente_disponible(self, agentes: list[object]):
        for i in range(len(agentes)):
            agente = agentes[i]
            if agente.estado == "Disponible":
                print(f"Estoy libre {agente.id}")
                return agente
    
    def seleccionar_mensaje(self) -> str:
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

    def palabras_clave(mensaje) -> int:
        diccionario_clave = {"emergencia": 10, "urgente": 8, "fallo critico": 9, "problema": 5, "consulta": 2, "duda": 1}
        puntos = 0
        for claves, valor in diccionario_clave.items():
            if claves in mensaje:
                puntos += valor
        return puntos
    
    def porcentaje_experiencia(agente: Agente) -> float:
        if agente.nivel_experiencia == "Experto":
            return 0.5
        elif agente.nivel_experiencia == "Intermedio":
            return 0.75
        else:
            return 1.0
        
        
class Llamado_repetido:
    def atender(self, agente: Agente, mensaje: str):
        peso_palabras_claves = Llamado_Unico.palabras_clave(mensaje)
        factor_nivel = Llamado_Unico.porcentaje_experiencia(agente)
        agente.tiempo_respuesta = agente.calcular_tiempo(len(mensaje), peso_palabras_claves, factor_nivel)




if __name__ == "__main__":
    iniciar()