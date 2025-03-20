import threading
import os
import random
import time


def iniciar():
    Llamado_repetido.atender()
    pass
    
class Queue:
    def __init__(self):
        self.queu: list[int] = []

    def enqueue(self, e: str, idx: int = 0):
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

class Agente:
    def __init__(self, id: int, nivel_experiencia: str, estado: str = "Disponible", tiempo_respuesta: int = 0):
        self.id: int = id
        self. nivel_experiencia: str = nivel_experiencia
        self.estado: str = estado
        self.tiempo_respuesta: int = tiempo_respuesta

    def calcular_tiempo(self, longitud_mensaje: int, peso_palabras_calves: int, factor_nivel: float):
        self.tiempo_respuesta = ((longitud_mensaje / 10) + (peso_palabras_calves / 2) * factor_nivel)
    
    def __repr__(self):
        return f"Mi id es: {self.id} y soy {self.nivel_experiencia}"

class Mensaje:
    def __init__(self, mensaje: str, peso_prioridad: int = 0):
        self.mensaje: str = mensaje
        self.peso_prioridad: int = peso_prioridad
    
    def genera_peso_prioridad(self):
        diccionario_clave = {"emergencia": 10, "urgente": 8, "fallo critico": 9, "problema": 5, "consulta": 2, "duda": 1}
        for claves, valor in diccionario_clave.items():
            if claves in self.mensaje:
                self.peso_prioridad += valor
    
    def __str__(self):
        return f"{self.mensaje}"
  

class Llamado_Unico:
    def crear_agentes(self) -> Agente:
        tipo_experiencias = ["Experto", "Intermedio", "Basico"]
        id = random.randint(1000, 9999)
        experiencia = random.randint(0, len(tipo_experiencias) - 1)
        agente = Agente(id, tipo_experiencias[experiencia])
        return agente

    def agente_disponible(self, agente: Agente):
        if agente.estado == "Disponible":
            return True
        else:
            return False
    
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
    
    def crear_cola_mensajes(mensaje: str) -> Queue:
        queue = Queue()
        if mensaje not in queue:
            queue.enqueue(mensaje)

    
    def porcentaje_experiencia(agente: Agente) -> float:
        if agente.nivel_experiencia == "Experto":
            return 0.5
        elif agente.nivel_experiencia == "Intermedio":
            return 0.75
        else:
            return 1.0
       # """ cambios Crear la cola en otro metodo"""
        
    def generar_atencion(self):
        mensaje = self.seleccionar_mensaje()
        agente = self.crear_agentes()

        peso_palabras_claves = Llamado_Unico.palabras_clave(mensaje)
        factor_nivel = Llamado_Unico.porcentaje_experiencia(agente)
        agente.calcular_tiempo(len(mensaje), peso_palabras_claves, factor_nivel)

        print(f"\nEL agente {agente.id} ({agente.nivel_experiencia}) se encargo del mensaje\n{mensaje}")
        time.sleep(agente.tiempo_respuesta)    
        print(f"\nEl agente {agente.id} termino el problema '{mensaje}' \n")
        

class Llamado_repetido:
    def atender():
        for _ in range(0, 10):
            atencion = Llamado_Unico()
            hilo1 = threading.Thread(target = atencion.generar_atencion)
            hilo2 = threading.Thread(target = atencion.generar_atencion)
            hilo3 = threading.Thread(target = atencion.generar_atencion)

            hilo1.start()
            hilo2.start()
            hilo3.start()

            hilo1.join()
            hilo2.join()
            hilo3.join()




if __name__ == "__main__":
    iniciar()


#Necitamos hacer que el mensaje sea un objeto que tenga como parametros el mensaje y el peso. Termianar la cola del mensaje y hacer la cola de agetes
#Crear la cola FIFO para los agentes
#Convertir los mensajes para que entren en la cola