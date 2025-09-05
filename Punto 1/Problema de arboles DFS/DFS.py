import heapq

def ucs(grafo, inicio, meta):
    cola = [(0, inicio)]  # (costo, nodo)
    visitados = set()
    costo_acumulado = {inicio: 0}
    padre = {inicio: None}
    
    while cola:
        costo, nodo = heapq.heappop(cola)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        if nodo == meta:
            break
        for vecino, costo_arista in grafo[nodo]:
            nuevo_costo = costo + costo_arista
            if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
                costo_acumulado[vecino] = nuevo_costo
                heapq.heappush(cola, (nuevo_costo, vecino))
                padre[vecino] = nodo
    
    # Reconstruir el camino
    def reconstruir_camino(padre, meta):
        camino = []
        actual = meta
        while actual is not None:
            camino.append(actual)
            actual = padre.get(actual)
        return camino[::-1]  # Invertir el camino
    
    return reconstruir_camino(padre, meta), costo_acumulado.get(meta, float('inf'))

# Grafo con costos (costos unitarios)
grafo_costo = {
    'S': [('A', 1), ('B', 1), ('D', 1), ('E', 1)],
    'A': [('F', 1), ('G', 1)],
    'F': [('M', 1)],
    'M': [('N', 1)],
    'N': [],
    'G': [],
    'B': [('H', 1), ('R', 1)],
    'H': [('O', 1), ('Q', 1)],
    'O': [('P', 1)],
    'P': [],
    'Q': [('U', 1)],
    'U': [('V', 1), ('W', 1)],
    'V': [],
    'W': [],
    'R': [('X', 1), ('T', 1)],
    'X': [],
    'T': [('GG', 1)],
    'GG': [],
    'D': [('J', 1)],
    'J': [('Y', 1)],
    'Y': [('Z', 1)],
    'Z': [('AA', 1), ('BB', 1)],
    'AA': [],
    'BB': [],
    'E': [('K', 1), ('L', 1)],
    'K': [('I', 1)],
    'I': [],
    'L': [('CC', 1)],
    'CC': [('DD', 1), ('EE', 1)],
    'DD': [],
    'EE': [('FF', 1)],
    'FF': []
}

camino, costo = ucs(grafo_costo, 'S', 'W')
print("UCS - Camino:", camino, "Costo:", costo)