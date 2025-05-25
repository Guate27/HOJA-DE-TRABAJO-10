import sys
import numpy as np
import os

class Grafo:
    def __init__(self):
        self.grafo = {}
        self.nodos = []

    def agregar_arco(self, ciudad1, ciudad2, tiempos):
        if ciudad1 not in self.grafo:
            self.grafo[ciudad1] = {}
            self.nodos.append(ciudad1)
        if ciudad2 not in self.grafo:
            self.grafo[ciudad2] = {}
            self.nodos.append(ciudad2)
        self.grafo[ciudad1][ciudad2] = tiempos

    def floyd_warshall(self):
        n = len(self.nodos)
        dist = np.full((n, n), float('inf'))
        next_node = [[None] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        for ciudad1 in self.grafo:
            for ciudad2, tiempos in self.grafo[ciudad1].items():
                dist[self.nodos.index(ciudad1)][self.nodos.index(ciudad2)] = tiempos['normal']
                next_node[self.nodos.index(ciudad1)][self.nodos.index(ciudad2)] = ciudad2

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

        return dist, next_node

    def calcular_centro(self, dist):
        n = len(self.nodos)
        centro = None
        menor_distancia_maxima = float('inf')

        for i in range(n):
            distancia_maxima = max(dist[i])
            if distancia_maxima < menor_distancia_maxima:
                menor_distancia_maxima = distancia_maxima
                centro = self.nodos[i]

        return centro

    def leer_grafo_de_archivo(self, nombre_archivo):
        if not os.path.exists(nombre_archivo):
            print(f"El archivo {nombre_archivo} no existe. Creando uno nuevo con datos de ejemplo.")
            self.crear_archivo_de_ejemplo(nombre_archivo)

        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                datos = linea.split()
                tiempos = {
                    'normal': int(datos[2]),
                    'lluvia': int(datos[3]),
                    'nieve': int(datos[4]),
                    'tormenta': int(datos[5])
                }
                self.agregar_arco(datos[0], datos[1], tiempos)

    def crear_archivo_de_ejemplo(self, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write("BuenosAires SaoPaulo 10 15 20 50\n")
            archivo.write("BuenosAires Lima 15 20 30 70\n")
            archivo.write("Lima Quito 10 12 15 20\n")
            print(f"Archivo {nombre_archivo} creado con datos de ejemplo.")

    def mostrar_matriz_adyacencia(self, dist):
        print("Matriz de Adyacencia (distancias más cortas):")
        for i in range(len(self.nodos)):
            print("\t".join(f"{dist[i][j]:.2f}" for j in range(len(self.nodos))))
        print()

    def ruta_mas_corta(self, origen, destino, next_node):
        if next_node[self.nodos.index(origen)][self.nodos.index(destino)] is None:
            return None
        ruta = []
        while origen != destino:
            ruta.append(origen)
            origen = next_node[self.nodos.index(origen)][self.nodos.index(destino)]
        ruta.append(destino)
        return ruta

