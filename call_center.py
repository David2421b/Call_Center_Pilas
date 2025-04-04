import threading
import os
import random
import time

lock = threading.Lock()

def iniciar():
    Llamado_Unico.atender()

class EmptyQueue(Exception):
    def __init__(self):
        super().__init__("Ya no hay mas mensajes Disponibles")

class Agente:
    def __init__(self, id: int, nivel_experiencia: str, estado: str = "Disponible", tiempo_respuesta: int = 0):
        self.id: int = id
        self.nivel_experiencia: str = nivel_experiencia
        self.estado: str = estado
        self.tiempo_respuesta: int = tiempo_respuesta

    def calcular_tiempo(self, longitud_mensaje: int, peso_palabras_calves: int, factor_nivel: float):
        self.tiempo_respuesta = ((longitud_mensaje / 10) + (peso_palabras_calves / 2)) * factor_nivel
    
    def __repr__(self):
        return f"Mi id es: {self.id} y soy {self.nivel_experiencia}"

class Mensaje:
    def __init__(self, mensaje: str, peso_prioridad: int = 0):
        self.mensaje: str = mensaje
        self.peso_prioridad: int = peso_prioridad
    
    def genera_peso_prioridad(self):
        self.peso_prioridad = 0
        diccionario_clave = {"emergencia": 10, "urgente": 8, "fallo crítico": 9, "problema": 5, "consulta": 2, "duda": 1}
        for claves, valor in diccionario_clave.items():
            if claves in self.mensaje:
                self.peso_prioridad += valor
    
    def __repr__(self):
        return str(f"{self.mensaje}")
    
    def __len__(self):
        return len(self.mensaje)
    
class PriorityQueue:
    def __init__(self):
        self.queue: list = []

    def enqueue(self, e: Mensaje, idx: int = 0):
        if idx == len(self.queue):
            self.queue.append(e)
            return
        posicion_queue: Mensaje = self.queue[idx]      
        if e.peso_prioridad > posicion_queue.peso_prioridad:
            self.queue.insert(idx, e)
            return
        return self.enqueue(e, idx + 1)

    def dequeue(self):
        if not self.queue:
            raise EmptyQueue()
        return self.queue.pop(0)
    
    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return str(self.queue)
    

class Queue:
    
    def __init__(self):
        self.__queue: list = []

    def enqueue(self, element: Agente):
        self.__queue.append(element)

    def dequeue(self) -> int:
        if(len(self.__queue) == 0):
            raise EmptyQueue()
        return self.__queue.pop(0)

    def first(self) -> int:
        if(len(self.__queue) == 0):
            raise EmptyQueue()
        
        return self.__queue[0]
    
    def __len__(self):
        return len(self.__queue)

    def __repr__(self):
        return str(self.__queue)

class Llamado_Repetido:
    def crear_agentes(self, queue: Queue) -> Queue:
        tipo_experiencias = ["Experto", "Intermedio", "Basico"]
        id = random.randint(1000, 9999)
        experiencia = random.randint(0, len(tipo_experiencias) - 1)
        agente = Agente(id, tipo_experiencias[experiencia])

        if queue is None:
            queue = Queue()
        queue.enqueue(agente)
        return queue
    
    def seleccionar_agente(self, queue: Queue):
        caso_base = True
        while caso_base is True:
            item: Agente = queue.dequeue()
            if item.estado == "Disponible":
                caso_base = False
                return item
            queue.enqueue(item)
    
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

    def crear_cola_mensajes(self, queue: PriorityQueue = None) -> PriorityQueue:
        solicitud_str = Mensaje(self.seleccionar_mensaje())
        solicitud_str.genera_peso_prioridad()

        if queue is None:
            queue = PriorityQueue()

        queue.enqueue(solicitud_str)            
        return queue

    def aumentar_mensajes(self, queue: PriorityQueue):
        self.crear_cola_mensajes(queue)
        return queue
    
    def porcentaje_experiencia(self, agente: Agente) -> float:
        if agente.nivel_experiencia == "Experto":
            return 0.5
        elif agente.nivel_experiencia == "Intermedio":
            return 0.75
        else:
            return 1.0


    def generar_atencion(self, agente_queue: Queue, mensaje_queue: PriorityQueue):
        with lock:
            for _ in range(len(agente_queue)):
                try:
                    item_mensaje: Mensaje = mensaje_queue.dequeue()
                except EmptyQueue:
                    print("No hay más mensajes disponibles.")
                    return  # Sale de la función sin errores

                try:
                    item_agente: Agente = agente_queue.dequeue()
                except EmptyQueue:
                    print("No hay más agentes disponibles.")
                    return  # Sale de la función sin errores

                if item_agente.estado == "Disponible":
                    item_agente.calcular_tiempo(len(item_mensaje.mensaje), item_mensaje.peso_prioridad, self.porcentaje_experiencia(item_agente))
                    item_agente.estado = "Ocupado"
                    print(f"\n-  El problema ({item_mensaje.mensaje}) será resulto por el agente {item_agente.id} ({item_agente.nivel_experiencia})")
                    time.sleep(item_agente.tiempo_respuesta)
                    print(f"     El agente: {item_agente.id} ha resuelto el problema en {item_agente.tiempo_respuesta} segundos\n")
                    time.sleep(1)
                    item_agente.estado = "Disponible"                
                    agente_queue.enqueue(item_agente)
                    
                else:
                    agente_queue.enqueue(item_agente)
                    mensaje_queue.enqueue(item_mensaje)
                    return

    def agrupacion(self, cola_mensaje: PriorityQueue):
        diccionario_contador = {}
        mayor = 0
        auxiliar_1 = PriorityQueue()
        new_grupo = PriorityQueue()
        
        for _ in range(len(cola_mensaje)): 
            item_1: Mensaje = cola_mensaje.dequeue()

            if item_1.peso_prioridad not in diccionario_contador:
                contador_new = 1
                diccionario_contador[item_1.peso_prioridad] = contador_new 
                auxiliar_1.enqueue(item_1)
            else:
                diccionario_contador[item_1.peso_prioridad] += 1
                auxiliar_1.enqueue(item_1)
            
        for claves, valores in diccionario_contador.items():
            if valores > mayor:
                mayor = valores
                grupo_mayor = (claves)
        # print(f"el grupo mayor es = {grupo_mayor}")
                
        for _ in range(len(auxiliar_1)):
            item_2: Mensaje = auxiliar_1.dequeue()

            if item_2.peso_prioridad == grupo_mayor:
                cola_mensaje.enqueue(item_2)

            else: 
                new_grupo.enqueue(item_2)
        # print(f"\nel diccionario 1 es = {diccionario_contador}\n")
        # print(f"\nel grupo 1 es = {cola_mensaje}\n")
        base = len(cola_mensaje)
        for i in range(len(cola_mensaje)):
            mensaje_temporal = cola_mensaje.dequeue()
            if i == 0 or i == base - 1:
                cola_mensaje.enqueue(mensaje_temporal)
            else:
                new_grupo.enqueue(mensaje_temporal)

        # print(f"\nel diccionario 1 es = {diccionario_contador}\n")
        # print(f"\nel grupo 1 es = {cola_mensaje}\n")
        return new_grupo

    
class Llamado_Unico:
    def atender():
        agente_queue = Queue()
        mensaje_queue = PriorityQueue()
        llamado = Llamado_Repetido()
        for _ in range(4):
            llamado.crear_agentes(agente_queue)
        for _ in range(7):
                llamado.aumentar_mensajes(mensaje_queue)
        print(f"\n{mensaje_queue}\n")
        print()
        nuevo_grupo = llamado.agrupacion(mensaje_queue)
        print(f"Los mensajes a atender seran = {mensaje_queue}")

        lista_hilos = []
        for _ in range(3):
            t = threading.Thread(target = llamado.generar_atencion, args = (agente_queue, mensaje_queue))
            lista_hilos.append(t)
            t.start()
        
        for t in lista_hilos:
            t.join()
        
        print("Se han terminado todos los llamados, hora de almorzar")

                
if __name__ == "__main__":
    iniciar()
