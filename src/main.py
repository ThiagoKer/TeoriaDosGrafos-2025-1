from matrizAdjacencias import MatrizAdjacencias
from listaAdjacencias import ListaAdjacencias
import info

if __name__ == "__main__":
    grafo = ListaAdjacencias(4)
    grafo.addAresta(0, 2, 5)
    grafo.addAresta(0, 3, 3)
    grafo.addAresta(1, 2, 2)
    grafo.addAresta(3, 1, 1)

    print(f"Ordem: {grafo.ordem()}")
    print(f"Tamanho: {grafo.tamanho()}")

    grafo.printGrafo()
    for i in range(grafo.numVertices):
        print(f"Vizinhos de {i}: {grafo.vizinhos(i)}")
    
    for i in range(grafo.numVertices):
        print(f"Grau do vertice {i}: {grafo.grau(i)}")

    print(f"Densidade: {info.densidade(grafo)}")

    print("Grafo complementar:")
    comp = info.complemento(grafo)
    comp.printGrafo()