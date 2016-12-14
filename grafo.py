import queue as Cola
import heapq as heap
import random
visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
   (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''

    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self.vertices = {} #diccionario cuyas claves son id de personajes y el valor el peso de la arista.
        #{Hulk:{Iron Man: 4, Black Widow: 7}, Spiderman:{Capitan America:4, Ant Man: 1}}
        self.cant_vertices = 0
        self.dirigido = es_dirigido


    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return self.cant_vertices

    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        return iter(self.vertices)

    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
        return list(self.vertices.keys())

    def __getitem__(self, id):
        '''Devuelve el valor del vertice asociado, del identificador indicado.
        Si no existe el identificador en el grafo, lanzara KeyError.'''
        valor = self.vertices.get(id, None)
        if not valor :
            raise KeyError()
        return valor


    def __setitem__(self, id, valor):
        '''Agrega un nuevo vertice con el par <id, valor> indicado.
        ID debe ser de identificador unico del vertice.
        En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.'''
        if id not in self.vertices:
            self.cant_vertices += 1
        self.vertices[id] = valor

    def __delitem__(self, id):
        '''Elimina el vertice del grafo. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.'''
        raise NotImplementedError()

    def __contains__(self, id):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''
        return id in self.vertices

    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
           - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
           Si el grafo es no-dirigido, tambien agregara la arista reciproca.'''
        if desde not in self.vertices or hasta not in self.vertices:
            raise KeyError()
        dicc_aux = self.vertices.get(desde, {})
        dicc_aux[hasta] = peso
        self.vertices[desde] = dicc_aux
        if not self.dirigido:
            dicc_aux = self.vertices.get(hasta, {})
            dicc_aux[desde] = peso
            self.vertices[hasta] = dicc_aux

    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
        - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
        En caso de no existir la arista, se lanzara ValueError.'''
        if desde not in self.vertices or hasta not in self.vetices:
            raise KeyError()
        dicc_aux = self.vertices.get(desde)
        if not dicc_aux or not dicc_aux.pop(hasta):
            raise ValueError()



    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
        - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
        En caso de no existir la union consultada, se devuelve None.'''
        if desde not in self.vertices or hasta not in self.vertices:
            raise KeyError()
        return self.vertices.get(desde, {}).get(hasta)


    def adyacentes(self, id):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado.
        Si no existe el vertice, se lanzara KeyError'''
        lista = self.vertices.get(id, None)
        if not lista:
            raise KeyError()
        return lista.keys()

    def recorrido(self, inicio):
        if len(self) == 0:
            return ({}, {})
        if not inicio:
            inicio = self.keys()[0]
        padre = {inicio: None}
        orden = {inicio: 0}
        return padre, orden, inicio

    def bfs(self, visitar = visitar_nulo, extra = None, inicio = None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
       Parametros:
           - visitar: una funcion cuya firma sea del tipo:
                   visitar(v, padre, orden, extra) -> Boolean
                   Donde 'v' es el identificador del vertice actual,
                   'padre' el diccionario de padres actualizado hasta el momento,
                   'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y
                   'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar).
                   La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
           - extra: el parametro extra que se le pasara a la funcion 'visitar'
           - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice,
           y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
       Salida:
           Tupla (padre, orden), donde :
               - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
               - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
       '''
        padre, orden, inicio = self.recorrido(inicio)
        cola = Cola.Queue()
        cola.put_nowait(inicio)
        while not cola.empty():
            v = cola.get_nowait()#desencolo de la cola
            for w in self.adyacentes(v):
                if w not in orden:
                    padre[w] = v
                    orden[w] = orden[v] + 1
                    if visitar:
                        visitar(w, padre, orden, extra)
                    cola.put_nowait(w)#encolo w en la cola
        return padre, orden



    def dfs_rec(self, v, visitar, extra, orden, padre):
        for w in self.adyacentes(v):
            if w not in orden:
                padre[w] = v
                orden[w] = orden[v] + 1
                if visitar:
                    visitar(w, padre, orden, extra)
                self.dfs_rec(w, visitar, extra, orden, padre)

    def dfs(self, visitar = visitar_nulo, extra = None, inicio = None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
       - visitar: una funcion cuya firma sea del tipo:
                   visitar(v, padre, orden, extra) -> Boolean
                   Donde 'v' es el identificador del vertice actual,
                   'padre' el diccionario de padres actualizado hasta el momento,
                   'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y
                   'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar).
                   La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
           - extra: el parametro extra que se le pasara a la funcion 'visitar'
           - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice,
           y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
       Salida:
           Tupla (padre, orden), donde :
               - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
               - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
       '''
        padre, orden, inicio = self.recorrido(inicio)
        self.dfs_rec(inicio, visitar, extra, orden, padre)
        return padre, orden

    '''def componentes_conexas(self):
       Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
       Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
       en caso de aplicarse a un grafo dirigido se lanzara TypeError
       raise NotImplementedError()'''

    '''def camino_minimo(self, origen, destino, heuristica = heuristica_nula):
        Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
       A* en caso que la heuristica no sea nula. Parametros:
           - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
           Por defecto, la funcion nula (devuelve 0 siempre)
       Devuelve:
           - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino.
           En caso que no exista camino entre el origen y el destino, se devuelve None.
        if desde not in self.vertices or hasta not in self.vetices:
            raise KeyError()
        #heap de minimos
        distancia = {}
        padre = {}
        for v in self.vertices:
            distancia[v] = #infinito
            padre[v] = None
            #heap_encolar(v, distancia[v])
        distancia[origen] = None
        while #heap_no_vacio :
            v = #heap_desencolar
            for w in self.adyacentes(v):
                if distancia[v] + self.obtener_peso_arista(v, w) < distancia[w]
                    distancia[w] =  distancia[v] + self.obtener_peso_arista(v, w)
                    padre[w] = v
                    #heap_modificar_prioridad(w, distancia[w])'''

    def pesos(self, v, adyacentes):
        total = 0
        for w in adyacentes:
            total += self.obtener_peso_arista(v, w)
        rand = random.uniform(0, total)
        acum = 0
        for w in adyacentes:
            acum += self.obtener_peso_arista(v, w)
            if acum >= rand:
                return w


    def random_walk(self, largo, origen = None, pesado = False):
        ''' Devuelve una lista con un recorrido aleatorio de grafo.
           Parametros:
               - largo: El largo del recorrido a realizar
               - origen: Vertice (id) por el que se debe comenzar el recorrido. Si origen = None, se comenzara por un vertice al azar.
               - pesado: indica si se tienen en cuenta los pesos de las aristas para determinar las probabilidades de movernos de un vertice a uno de sus vecinos (False = todo equiprobable).
           Devuelve:
               Una lista con los vertices (ids) recorridos, en el orden del recorrido.'''
        if not origen:
            v = self.keys[0]
        else:
            v = origen
        recorrido = []
        for i in range(1, largo):
            adyacentes = self.adyacentes(v)
            if not pesado:
                v = adyacentes[random.uniform(0, len(adyacentes))]
            else:
                v = self.pesos(v, adyacentes)
            recorrido.append(v)
        return recorrido
