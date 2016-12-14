from grafo import Grafo
import heapq as heap
import csv
import random
import math
from collections import Counter
# -- Label Propagation -- #
CANT_ITERACIONES = 6 
COMMAX = 1000
COMMIN = 4
# ----------------------- #
ARCHIVO = "marvel.pjk"
LARGO_RANDOM_WALKS = 100
N = 50
LISTA_OPCIONES = ['SIMILARES', 'RECOMENDAR',
                  'CAMINO', 'CENTRALIDAD',
                  'DISTANCIAS', 'ESTADISTICAS',
                  'COMUNIDADES', 'SALIR']

SIMILARES = 1
RECOMENDAR = 2
CAMINO = 3
CENTRALIDAD = 4
DISTANCIAS = 5
ESTADISTICAS = 6
COMUNIDADES = 7
SALIR = 8


def main():
    try:
        grafo  = cargar_archivo(ARCHIVO)
        opcion = ""
    except IOError as error:
        print("Error:", error)
        opcion = SALIR

    while opcion != SALIR:
        mostrar_menu()
        opcion = pedir_opcion()
        if opcion == SIMILARES:
            similares(grafo, pedir_nombre(grafo), pedir_cantidad(len(grafo)))
        elif opcion == RECOMENDAR:
            recomendar(grafo, pedir_nombre(grafo), pedir_cantidad(len(grafo)))
        elif opcion == CENTRALIDAD:
            print(centralidad(grafo, pedir_cantidad(len(grafo))))
        elif opcion == DISTANCIAS:
            distancias(grafo, pedir_nombre(grafo))
        elif opcion == CAMINO:
            print("Ingrese personaje origen y personaje destino")
            camino(grafo,pedir_nombre(grafo),pedir_nombre(grafo))
        elif opcion == ESTADISTICAS:
            estadisticas(grafo)
        elif opcion == COMUNIDADES:
            listar_comunidades(grafo)
    print("Hasta luego.")

# -----------------------------------------------------------------------------
# |                          Funciones Auxiliares                             |
# -----------------------------------------------------------------------------
def recorrer_grafo_aleatoriamente(grafo, origen):#O(Largo)
    vertices_recorridos = {}
    camino = grafo.random_walk(LARGO_RANDOM_WALKS, origen, True)#O(Largo)
    for v in camino:#O(Largo)
        vertices_recorridos[v] = vertices_recorridos.get(v, 0) + 1
    vertices_recorridos.pop(origen, None)
    return vertices_recorridos

def visitar_distancias(v, padre, orden, extra):
    extra[orden[v]] = extra.get(orden[v], 0) + 1
    return True
'''----------- Auxiliares a Camino ------------'''       
def _construir_camino(padre, v):
    #recorro de padre en padre (desde destino a origen)
    aux = []
    while padre.get(v, -1) != -1:
        aux.append(v)
        v = padre[v]
    aux.append(v)
    aux.pop() # elimino padre de origen (None)
    aux.reverse() # camino de origen a destino 
    return aux
    
def _camino(g, origen, destino):
    '''Algoritmo de Dijkstra modificado. Devuelve un camino en
    formato de lista que conecta origen a destino maximizando el 
    peso de las aristas.'''
    if destino in g.adyacentes(origen):
        return [origen,destino]
    maxheap = []
    distancia = {}
    padre = {}
    for v in g.keys():
        distancia[v] = math.inf
        padre[v] = None
        heap.heappush(maxheap, (distancia[v], v))
    distancia[origen] = 0
    while (len(maxheap) != 0):
        v = heap.heappop(maxheap)[1]
        if (v == destino):
            return _construir_camino(padre,v)
        for w in g.adyacentes(v):
            peso_arista = 1/g.obtener_peso_arista(v,w)
            #invierto pesos para que sea un maxheap
            if distancia[v] + peso_arista < distancia[w]:
                distancia[w] = distancia[v] + 1/peso_arista
                padre[w] = v
    return [] #no hay camino

def _imprimir_camino(g, camino):
    print (" -> ".join(v for v in camino))
'''----------------------------------------''' 
'''------- Auxiliares a Estadisticas ------'''
def grado_promedio(g):
    resultado = 0
    vertices = g.keys()
    for v in vertices:
        resultado += len(g.adyacentes(v))
    resultado /= len(vertices)
    return resultado
    
def densidad(g, cant_aristas = 0):
    if not cant_aristas:
        cant_aristas = g.cantidad_aristas()
    # cant. de aristas de grafo completo
    cant_max = (len(g)*(len(g)-1))/2 
    return cant_aristas/cant_max
    
def desvio_estandar(g, gradoprom = 0):
    resultado = 0
    if not gradoprom:
        gradoprom = grado_promedio(g)
    for v in g.keys():
        grado = len(g.adyacentes(v))
        resultado += math.pow(grado - gradoprom, 2)
    resultado /= (len(g) - 1)
    resultado = math.sqrt(resultado)
    return resultado
'''--------------------------------------'''
'''----- Auxiliares a  Comunidades ------'''

def mas_frecuente(lista):
    return Counter(lista).most_common(1)[0][0]
 
def _filtrar_comunidades(comunidades):
    a_eliminar = []
    for c in comunidades:
        cant_miembros = len(comunidades[c][1])
        if  cant_miembros > COMMAX or cant_miembros < COMMIN:
            a_eliminar.append(c)
    for i in range(len(a_eliminar)):
        eliminar = a_eliminar[i]
        comunidades.pop(eliminar, None)

def _label_propagation(g):
    if (not isinstance(g,Grafo)):
        return TypeError
    # inicializar
    vertices = g.keys()
    label = {vertices[i] : i for i in range(len(vertices))}
    parar = False
    for i in range(1,CANT_ITERACIONES):
        random.shuffle(vertices)
        for v in vertices:
            adjlabel = [label[w] for w in g.adyacentes(v)]
            label[v] = mas_frecuente(adjlabel)
    #fin propagacion
    comunidades = {l:[0,[]] for l in set(label.values())}
    # {comunidad: [cant_miembros, [miembro 1, miembro 2 ...]}
    for v in label:
        comunidades[label[v]][0] += 1
        comunidades[label[v]][1].append(v)    
    # descarto comunidades grandes y despreciables
    _filtrar_comunidades(comunidades)  
    return comunidades
'''-----------------------------------'''
# -----------------------------------------------------------------------------
# |                          Comandos a Implementar                           |
# -----------------------------------------------------------------------------
def similares (grafo, origen, cantidad):
    recorrido = {}
    for i in range(N):
        recorrido_parcial = recorrer_grafo_aleatoriamente(grafo, origen)
        for w in recorrido_parcial:
            recorrido[w] = recorrido.get(w, 0) + recorrido_parcial[w]
    print(list(map(lambda x: x[0], heap.nlargest(cantidad, recorrido.items(), key = lambda x: x[1]))))


def recomendar(grafo, origen, cantidad):
    recorrido = {}
    for i in range(N):
        recorrido_parcial = recorrer_grafo_aleatoriamente(grafo, origen)
        for w in recorrido_parcial:
            recorrido[w] = recorrido.get(w, 0) + recorrido_parcial[w]
    for w in grafo.adyacentes(origen):
        if w in recorrido:
            recorrido.pop(w)
    print(list(map(lambda x: x[0], heap.nlargest(cantidad, recorrido.items(), key = lambda x: x[1]))))


def centralidad(grafo, cantidad):#Con random walks
    recorrido = {}
    cant_vertices = 0
    for v in grafo:
        if cant_vertices > N: break;
        recorrido_parcial = recorrer_grafo_aleatoriamente(grafo, v)#0(Largo)
        for w in recorrido_parcial:
            recorrido[w] = recorrido.get(w, 0) + recorrido_parcial[w]
        cant_vertices += 1
    print(list(map(lambda x: x[0], heap.nlargest(cantidad, recorrido.items(), key = lambda x: x[1]))))


def distancias (grafo, origen):
    dicc_distancias = {}
    grafo.bfs(visitar_distancias, dicc_distancias, origen)#O(V + A)
    i = 1
    while dicc_distancias.get(i, 0) != 0:
        print("Distancia {} : {}".format(i, dicc_distancias[i]))
        i += 1
        
def camino(g, personaje1, personaje2):
    camino = _camino(g, personaje1, personaje2)
    if (len(camino) == 0):
        print("{} no puede llegar a {}".format(personaje1, personaje2))
        return
    _imprimir_camino(g, camino)

def estadisticas(g):
    cant_aristas = g.cantidad_aristas()
    grado_prom = grado_promedio(g)
    print("Cantidad de vértices: {}".format(len(g)))
    print("Cantidad de aristas: {}".format(cant_aristas))
    print("Promedio del grado de cada vértice: {0:.2f}".format(grado_prom))
    print("Desvío estándar del grado de cada vértice: {0:.2f}".format(desvio_estandar(g,grado_prom)))
    print("Densidad del grafo: {0:.2f}".format(densidad(g, cant_aristas)))
    
def listar_comunidades(g):
    comunidades = _label_propagation(g)
    i = 1
    for c in comunidades:
        print("----- Comunidad {} -----".format(i))
        print("Cantidad de miembros: {}".format(comunidades[c][0]))
        print("\t-{}".format("\n\t-".join(m for m in comunidades[c][1])))
        i += 1
# -----------------------------------------------------------------------------
# |                         Cargar datos del archivo                          |
# -----------------------------------------------------------------------------
def cargar_archivo(archivo):
    try:
        with open(archivo, "r") as archivo_marvel:
            archivo_marvel_csv = csv.reader(archivo_marvel, delimiter = ' ')
            encabezado = next(archivo_marvel_csv, None)
            registro = next(archivo_marvel_csv, None)
            grafo = Grafo()
            dicc_aux = {}
            for i in range(int(encabezado[1])):
                grafo[registro[1]] = {}
                dicc_aux[int(registro[0])] = registro[1]
                registro = next(archivo_marvel_csv, None)
            registro = next(archivo_marvel_csv, None)
            while registro:
                grafo.agregar_arista( dicc_aux[int(registro[0])],
                                      dicc_aux[int(registro[1])],
                                      int(registro[2]))
                registro = next(archivo_marvel_csv, None)
            del dicc_aux
        return grafo
    except IOError:
        raise IOError("No se encontró el archivo: {}".format(archivo))
# -----------------------------------------------------------------------------
# |                       Interfaz e impresión en pantalla                    |
# -----------------------------------------------------------------------------

def mostrar_menu():
    """Imprime el menú principal"""
    print('------\nMenú principal \n------')
    imprimir_opciones(LISTA_OPCIONES)
    print('------')

def imprimir_opciones(lista):
    """Imprime una lista de opciones"""
    for i, elem  in enumerate(lista):
        print("{}. {}".format(i + 1, elem))

# -----------------------------------------------------------------------------
# |                             Ingreso datos                                 |
# -----------------------------------------------------------------------------

def pedir_opcion(cantidad = SALIR):
    """Pide el ingreso de una opcion"""
    return verif_ingreso(input("Su elección: "), cantidad, "Ingrese un número de opción: ")

def pedir_cantidad(cantidad):
    return verif_ingreso(input("Cantidad :"), cantidad, "Cantidad :")


def pedir_nombre(grafo):
    return verif_nombre(grafo, input("Personaje: "), "Personaje: ")


def es_numero(cadena, cantidad_opciones):
    """Verifica que la cadena sea una de las opciones posibles, establecidas por la
    cantidad pasada por parámetro"""
    return cadena.isdigit() and int(cadena) <= cantidad_opciones


# ----------------------------------------------------------------------------
# |                             Verificaciones                               |
# ----------------------------------------------------------------------------

def verif_ingreso(cadena, cantidad, mensaje):
    """Recibe una cadena ingresada por el usuario y no la devuelve hasta que
    sea un número perteneciente a las opciones posibles"""
    while not es_numero(cadena, cantidad):
        cadena = input(mensaje)
    return int(cadena)

def verif_nombre(grafo, cadena, mensaje):
    while not cadena.upper() in grafo:
        print("Personaje inexistente, reintente.")
        cadena = input(mensaje)
    return cadena.upper()

main()
