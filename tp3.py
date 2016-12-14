from grafo import Grafo
import heapq as heap
import csv

LARGO_RANDOM_WALKS = 100
N = 50
LISTA_OPCIONES = ['SIMILARES',
                  'RECOMENDAR',
                  'CAMINO',
                  'CENTRALIDAD',
                  'DISTANCIAS',
                  'ESTADISTICAS',
                  'COMUNIDADES',
                  'SALIR']

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
        grafo  = cargar_archivo("marvel.pjk")
        opcion = ""
        mostrar_menu()
    except IOError as error:
        print("Error:", error)
        opcion = SALIR

    while opcion != SALIR:
        opcion = pedir_opcion()
        if opcion == SIMILARES:
            similares(grafo, pedir_personaje(grafo), pedir_cantidad(len(grafo)))
        elif opcion == RECOMENDAR:
            recomendar(grafo, pedir_personaje(grafo), pedir_cantidad(len(grafo)))
        elif opcion == CENTRALIDAD:
            centralidad(grafo, pedir_cantidad(len(grafo)))
        elif opcion == DISTANCIAS:
            distancias(grafo, pedir_personaje(grafo))
        elif opcion == COMUNIDADES:
            print(grafo[input("Personaje : ")])
    print("Hasta luego.")

# -----------------------------------------------------------------------------
# |                          Funciones Auxiliares                             |
# -----------------------------------------------------------------------------
def recorrer_grafo_aleatoriamente(grafo, origen):#O(Largo)
    vertices_recorridos = {}
    camino = grafo.random_walk(LARGO_RANDOM_WALKS, origen, True)#O(Largo)
    #print(camino)
    for v in camino:#O(Largo)
        vertices_recorridos[v] = vertices_recorridos.get(v, 0) + 1
    vertices_recorridos.pop(origen, None)
    return vertices_recorridos

def visitar_distancias(v, padre, orden, extra):
    extra[orden[v]] = extra.get(orden[v], 0) + 1
    return True

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
    """Pide el ingreso de una cantidad"""
    return verif_ingreso(input("Cantidad :"), cantidad, "Cantidad :")

def pedir_personaje(grafo):
    """Pide el ingreso de un personaje """
    return verif_personaje(grafo, input("Personaje :"), "Personaje :")

# ----------------------------------------------------------------------------
# |                             Verificaciones                               |
# ----------------------------------------------------------------------------

def es_numero(cadena, cantidad_opciones):
    """Verifica que la cadena sea una de las opciones posibles, establecidas por la
    cantidad pasada por parámetro"""
    return cadena.isdigit() and int(cadena) <= cantidad_opciones

def verif_ingreso(cadena, cantidad, mensaje):
    """Recibe una cadena ingresada por el usuario y no la devuelve hasta que
    sea un número perteneciente a las opciones posibles"""
    while not es_numero(cadena, cantidad):
        cadena = input(mensaje)
    return int(cadena)

def verif_personaje(grafo, cadena, mensaje):
    while not cadena in grafo:
        cadena = input(mensaje)
    return cadena

main()
