import sys
import math
import time
import heapq
import tracemalloc
import logging
from typing import List, Tuple, Optional

from listaAdjacencias import ListaAdjacencias
from matrizAdjacencias import MatrizAdjacencias

# Configura o logging para salvar em log.txt (modo 'a' para acumular) e também exibir no terminal
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Exibe no terminal
        logging.FileHandler("log.txt", mode="a")  # Acumula no arquivo log.txt
    ]
)

def escolher_representacao(n: int, m: int) -> str:
    return "matriz" if m > (n * n) // 4 else "lista"

def carregar_grafo_dimacs(caminho: str):
    with open(caminho, "r") as f:
        header = f.readline().strip().split()
        if len(header) != 2:
            raise ValueError("Cabeçalho inválido. Esperado: '<num_vertices> <num_arestas>'")
        n, m = map(int, header)
        tipo = escolher_representacao(n, m)
        g = MatrizAdjacencias(n) if tipo == "matriz" else ListaAdjacencias(n)
        for line in f:
            if not line.strip():
                continue
            u, v, w = map(float, line.strip().split())
            g.addAresta(int(u), int(v), float(w))
    return g, tipo

def vizinhos_com_peso(g, tipo: str, u: int):
    if tipo == "lista":
        return [(v, float(p)) for (v, p) in g.vizinhos(u)]
    res = []
    for v in range(g.numVertices):
        w = g.matriz[u][v]
        if w != 0:
            res.append((v, float(w)))
    return res

def iter_arestas(g, tipo: str):
    edges = []
    if tipo == "lista":
        for u in range(g.numVertices):
            for v, w in g.vizinhos(u):
                edges.append((u, v, float(w)))
    else:
        for u in range(g.numVertices):
            for v in range(g.numVertices):
                w = g.matriz[u][v]
                if w != 0:
                    edges.append((u, v, float(w)))
    return edges

def dijkstra_mod(g, tipo: str, origem: int, destino: int):
    n = g.numVertices
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[origem] = 0.0
    pq = [(0.0, origem)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == destino:
            break
        for v, w in vizinhos_com_peso(g, tipo, u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[destino] == float('inf'):
        return None, float('inf')
    path = []
    cur = destino
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[destino]

def bellman_mod(g, tipo: str, origem: int, destino: int):
    n = g.numVertices
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[origem] = 0.0
    E = iter_arestas(g, tipo)
    for _ in range(n - 1):
        updated = False
        for u, v, w in E:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break
    for u, v, w in E:
        if dist[u] + w < dist[v]:
            return None, float('-inf')
    if dist[destino] == float('inf'):
        return None, float('inf')
    path = []
    cur = destino
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[destino]

def floyd_warshall_precompute(g, tipo: str):
    n = g.numVertices
    dist = [[float('inf')] * n for _ in range(n)]
    nxt = [[-1] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
        nxt[i][i] = i
    if tipo == "lista":
        for u in range(n):
            for v, w in g.vizinhos(u):
                if float(w) < dist[u][v]:
                    dist[u][v] = float(w)
                    nxt[u][v] = v
    else:
        for u in range(n):
            for v in range(n):
                w = g.matriz[u][v]
                if w != 0 and float(w) < dist[u][v]:
                    dist[u][v] = float(w)
                    nxt[u][v] = v
    for k in range(n):
        for i in range(n):
            if dist[i][k] == float('inf'):
                continue
            for j in range(n):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
                    nxt[i][j] = nxt[i][k]
    return dist, nxt

def reconstruir_caminho(nxt, origem: int, destino: int):
    if nxt[origem][destino] == -1:
        return None
    path = [origem]
    while origem != destino:
        origem = nxt[origem][destino]
        if origem == -1:
            return None
        path.append(origem)
    return path

def medir(func, *args, **kwargs):
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    tempo = time.perf_counter() - inicio
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_mb = pico / (1024 * 1024)
    return resultado, tempo, mem_mb

def imprimir_bloco(nome_algo: str, caminho, custo, tempo, memoria):
    logging.info("-" * 77)
    logging.info(f"Algoritmo de {nome_algo}:")
    if caminho is None or custo in (float('inf'), float('-inf')):
        logging.info("Caminho mínimo: inexistente")
        if custo == float('-inf'):
            logging.info("Custo: -inf (ciclo negativo detectado)")
        else:
            logging.info("Custo: inf")
    else:
        logging.info(f"Caminho mínimo: {caminho}")
        custo_fmt = int(custo) if abs(custo - int(custo)) < 1e-9 else round(custo, 6)
        logging.info(f"Custo: {custo_fmt}")
    logging.info(f"Tempo execução: {tempo:.3f} s")
    logging.info(f"Memória utilizada: {memoria:.4f} MB")

def executar():
    if len(sys.argv) != 4:
        logging.error("Modo de uso: python main.py <arquivo> <no_origem> <no_destino>")
        return
    
    # Captura o comando usado no terminal
    comando = ' '.join(sys.argv)
    logging.info(f"Comando executado: {comando}")

    arquivo = sys.argv[1]
    origem = int(sys.argv[2])
    destino = int(sys.argv[3])
    g, tipo = carregar_grafo_dimacs(arquivo)
    
    (caminho, custo), t, mem = medir(dijkstra_mod, g, tipo, origem, destino)
    imprimir_bloco("Dijkstra", caminho, custo, t, mem)
    
    (caminho, custo), t, mem = medir(bellman_mod, g, tipo, origem, destino)
    imprimir_bloco("Bellman-Ford", caminho, custo, t, mem)
    
    (dist, nxt), t_fw, mem_fw = medir(floyd_warshall_precompute, g, tipo)
    caminho_fw = reconstruir_caminho(nxt, origem, destino)
    custo_fw = dist[origem][destino] if caminho_fw is not None else float('inf')
    imprimir_bloco("Floyd-Warshall", caminho_fw, custo_fw, t_fw, mem_fw)
    
    logging.info("-" * 77)

if __name__ == "__main__":
    executar()
