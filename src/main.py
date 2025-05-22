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
    for i in range(grafo.numVertices):
        print(f"Vizinhos de {i}: {grafo.vizinhos(i)}")
    
    for i in range(grafo.numVertices):
        print(f"Grau do vertice {i}: {grafo.grau(i)}")