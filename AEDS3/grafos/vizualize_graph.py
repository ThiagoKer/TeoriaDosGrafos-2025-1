import math
import matplotlib.pyplot as plt
from listaAdjacencias import ListaAdjacencias
from matrizAdjacencias import MatrizAdjacencias

def escolher_representacao(n: int, m: int) -> str:
    return "matriz" if m > (n * n) // 4 else "lista"

def carregar_grafo_arquivo(caminho):
    with open(caminho, "r") as f:
        header = f.readline().strip().split()
        n, m = map(int, header)
        tipo = escolher_representacao(n, m)
        g = MatrizAdjacencias(n) if tipo == "matriz" else ListaAdjacencias(n)
        for line in f:
            if not line.strip():
                continue
            u, v, w = map(float, line.strip().split())
            g.addAresta(int(u), int(v), float(w))
    return g, tipo

def obter_arestas(g, tipo):
    arestas = []
    if tipo == "lista":
        for u in range(g.numVertices):
            for v, w in g.vizinhos(u):
                arestas.append((u, v, w))
    else:
        for u in range(g.numVertices):
            for v in range(g.numVertices):
                w = g.matriz[u][v]
                if w != 0:
                    arestas.append((u, v, w))
    return arestas

def exibir_grafo_visual(g, tipo):
    n = g.numVertices
    r = 5.0
    pos = {i: (r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n)) for i in range(n)}
    fig, ax = plt.subplots(figsize=(10, 8))
    for i, (x, y) in pos.items():
        circle = plt.Circle((x, y), 0.3, fill=True, alpha=0.7)
        ax.add_artist(circle)
        ax.text(x, y, str(i), ha='center', va='center')
    for (u, v, w) in obter_arestas(g, tipo):
        x1, y1 = pos[u]; x2, y2 = pos[v]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.5, alpha=0.7))
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my, str(round(w, 2)), fontsize=9)
    ax.set_title("Grafo com Pesos nas Arestas")
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    plt.show()

def iniciar_visualizacao():
    caminho_entrada = 'data/toy.txt'  # ajuste conforme necessário
    estrutura, tipo = carregar_grafo_arquivo(caminho_entrada)
    exibir_grafo_visual(estrutura, tipo)

if __name__ == "__main__":
    iniciar_visualizacao()
