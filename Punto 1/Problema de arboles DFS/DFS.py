def dfs_correcto(grafo, inicio, meta):
    pila = [inicio]  # Usar LISTA como PILA
    visitados = set()
    padre = {inicio: None}  # Mejor usar None para el nodo inicial
    
    while pila:
        nodo = pila.pop()  # Último en entrar, primero en salir (LIFO)
        
        if nodo == meta:
            break
            
        if nodo not in visitados:
            visitados.add(nodo)
            # Explorar vecinos en orden natural (no inverso)
            for vecino, _ in grafo[nodo]:
                if vecino not in visitados:
                    pila.append(vecino)
                    if vecino not in padre:  # Evitar sobrescribir padres
                        padre[vecino] = nodo
    
    # Reconstruir camino
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = padre.get(actual)
    
    # Calcular costo total (suma de costos unitarios)
    costo = len(camino) - 1 if camino and camino[0] == inicio else 0
    
    return camino[::-1], costo

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

camino, costo = dfs_correcto(grafo_costo, 'S', 'W')
print("DFS - Camino:", camino, "Costo:", costo)