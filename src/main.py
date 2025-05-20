from matrizAdjacencias import MatrizAdjacencias
from listaAdjacencias import ListaAdjacencias

if __name__ == "__main__":
    grafo = MatrizAdjacencias(5)
    grafo.addAresta(0, 1, 2)
    grafo.addAresta(0, 2, 4)
    grafo.addAresta(1, 4, 7)
    grafo.addAresta(4, 0, 3)

    print(f"Ordem: {grafo.ordem()}")
    print(f"Tamanho: {grafo.tamanho()}")

    grafo.printGrafo()

    print(f"Vizinhos de {0}: {grafo.vizinhos(0)}")
    print(f"Vizinhos de {1}: {grafo.vizinhos(1)}")
    print(f"Vizinhos de {2}: {grafo.vizinhos(2)}")
    print(f"Vizinhos de {3}: {grafo.vizinhos(3)}")
    print(f"Vizinhos de {4}: {grafo.vizinhos(4)}")