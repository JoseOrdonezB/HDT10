class Grafo:
    def __init__(self):
        # Inicializa el grafo con un diccionario vacío para almacenar los vértices y sus conexiones.
        self.vertices = {}

    def agregar_vertice(self, nombre):
        # Agrega un vértice al grafo si no existe.
        if nombre not in self.vertices:
            self.vertices[nombre] = {}

    def agregar_arista(self, origen, destino, peso):
        # Agrega una arista entre dos vértices con un peso dado.
        # Si los vértices no existen, los agrega primero.
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self.vertices[origen][destino] = peso

    def floyd_warshall(self):
        # Implementa el algoritmo de Floyd-Warshall para encontrar las distancias más cortas entre todos los pares de vértices.
        distancias = {v: {w: float('inf') if v != w else 0 for w in self.vertices} for v in self.vertices}
        for intermedio in self.vertices:
            for inicio in self.vertices:
                for fin in self.vertices:
                    nueva_distancia = distancias[inicio][intermedio] + distancias[intermedio][fin]
                    if nueva_distancia < distancias[inicio][fin]:
                        distancias[inicio][fin] = nueva_distancia
        return distancias

    def obtener_centro_grafo(self, distancias):
        # Determina el vértice central del grafo basado en las distancias calculadas por Floyd-Warshall.
        centros = {v: max(distancias[v].values()) for v in distancias}
        return min(centros, key=centros.get)

    def interrumpir_trafico(self, ciudad1, ciudad2):
        # Elimina la conexión entre dos ciudades si existe.
        if ciudad1 in self.vertices and ciudad2 in self.vertices:
            if ciudad2 in self.vertices[ciudad1]:
                del self.vertices[ciudad1][ciudad2]
                print(f"Se ha interrumpido el tráfico entre {ciudad1} y {ciudad2}.")
            else:
                print(f"No hay conexión entre {ciudad1} y {ciudad2}.")
        else:
            print("Al menos una de las ciudades no está en el grafo.")

    def establecer_conexion(self, ciudad1, ciudad2, tiempo_normal):
        # Establece una conexión entre dos ciudades con un tiempo normal dado.
        if ciudad1 in self.vertices and ciudad2 in self.vertices:
            self.vertices[ciudad1][ciudad2] = tiempo_normal
            print(f"Se ha establecido una conexión entre {ciudad1} y {ciudad2} con tiempo normal {tiempo_normal}.")
        else:
            print("Al menos una de las ciudades no está en el grafo.")

    def modificar_clima(self, ciudad1, ciudad2, clima, tiempo):
        # Modifica el tiempo de viaje entre dos ciudades dadas ciertas condiciones climáticas.
        if ciudad1 in self.vertices and ciudad2 in self.vertices:
            if ciudad2 in self.vertices[ciudad1]:
                self.vertices[ciudad1][ciudad2] = tiempo
                print(f"Se ha modificado el tiempo de viaje entre {ciudad1} y {ciudad2} con clima {clima} a {tiempo}.")
            else:
                print(f"No hay conexión entre {ciudad1} y {ciudad2}.")
        else:
            print("Al menos una de las ciudades no está en el grafo.")

    def mostrar_matriz_adyacencia(self):
        # Muestra la matriz de adyacencia del grafo.
        print("Matriz de Adyacencia:")
        for ciudad1 in self.vertices:
            for ciudad2 in self.vertices:
                if ciudad2 in self.vertices[ciudad1]:
                    print(self.vertices[ciudad1][ciudad2], end="\t")
                else:
                    print("-", end="\t")
            print()


def leer_archivo(nombre_archivo):
    # Lee un archivo que contiene información sobre las conexiones entre ciudades y crea un grafo a partir de esta información.
    grafo = Grafo()
    try:
        with open(nombre_archivo, 'r') as archivo:
            next(archivo)  # Saltar la primera línea que contiene los encabezados
            for linea in archivo:
                ciudad1, ciudad2, tiempo_normal, _, _, _ = linea.split()
                grafo.agregar_arista(ciudad1, ciudad2, int(tiempo_normal))
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
    except ValueError:
        print("Error al leer el archivo. Asegúrate de que esté en el formato correcto.")
    return grafo


def calcular_ruta_mas_corta(grafo, origen, destino, distancias):
    # Calcula la distancia más corta entre dos ciudades utilizando las distancias previamente calculadas por el algoritmo de Floyd-Warshall.
    if origen in grafo.vertices and destino in grafo.vertices:
        distancia = distancias[origen][destino]
        print(f"La distancia más corta entre {origen} y {destino} es: {distancia}")
    else:
        print("Al menos una de las ciudades no está en el grafo.")


def main():
    grafo = leer_archivo('logistica.txt')
    if not grafo.vertices:
        print("No se pudo construir el grafo correctamente. Verifica el archivo de entrada.")
        return

    distancias = grafo.floyd_warshall()

    while True:
        print("\nOpciones:")
        print("1. Calcular ruta más corta entre dos ciudades.")
        print("2. Indicar la ciudad que queda en el centro del grafo.")
        print("3. Modificar el grafo.")
        print("4. Finalizar el programa.")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            ciudad_origen = input("Ingrese la ciudad origen: ")
            ciudad_destino = input("Ingrese la ciudad destino: ")
            calcular_ruta_mas_corta(grafo, ciudad_origen, ciudad_destino, distancias)
        elif opcion == "2":
            centro = grafo.obtener_centro_grafo(distancias)
            print("El centro del grafo es la ciudad:", centro)
        elif opcion == "3":
            print("\nOpciones de modificación:")
            print("a. Interrumpir tráfico entre un par de ciudades.")
            print("b. Establecer conexión entre ciudad1 y ciudad2.")
            print("c. Modificar clima entre un par de ciudades.")
            modificacion = input("Ingrese la letra correspondiente a la opción de modificación deseada: ")
            if modificacion == "a":
                ciudad1 = input("Ingrese la ciudad 1: ")
                ciudad2 = input("Ingrese la ciudad 2: ")
                grafo.interrumpir_trafico(ciudad1, ciudad2)
            elif modificacion == "b":
                ciudad1 = input("Ingrese la ciudad 1: ")
                ciudad2 = input("Ingrese la ciudad 2: ")
                tiempo_normal = int(input("Ingrese el tiempo normal de conexión: "))
                grafo.establecer_conexion(ciudad1, ciudad2, tiempo_normal)
            elif modificacion == "c":
                ciudad1 = input("Ingrese la ciudad 1: ")
                ciudad2 = input("Ingrese la ciudad 2: ")
                clima = input("Ingrese el clima (normal, lluvia, nieve o tormenta): ")
                tiempo = int(input("Ingrese el tiempo de conexión para este clima: "))
                grafo.modificar_clima(ciudad1, ciudad2, clima, tiempo)
            else:
                print("Opción no válida.")
        elif opcion == "4":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")


if __name__ == "__main__":
    main()
