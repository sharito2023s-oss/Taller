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

# Grafo con costos realistas basados en criterios específicos
grafo_costo = {
    'S': [('A', 8), ('B', 3), ('D', 6), ('E', 5)],
    # S->B es el camino principal (3), S->E alternativa (5), S->D más lejano (6), S->A el más costoso (8)
    
    'A': [('F', 4), ('G', 2)],
    # A->G más directo (2), A->F con desvío (4)
    
    'F': [('M', 1)],
    'M': [('N', 3)],
    'N': [],
    'G': [],
    
    'B': [('H', 2), ('R', 7)],
    # B->H camino óptimo hacia W (2), B->R camino alternativo más largo (7)
    
    'H': [('O', 5), ('Q', 3)],
    # H->Q camino directo a U (3), H->O desvío (5)
    
    'O': [('P', 2)],
    'P': [],
    'Q': [('U', 4)],
    # Q->U conexión importante pero con cierto costo (4)
    
    'U': [('V', 6), ('W', 2)],
    # U->W destino final cercano (2), U->V desvío (6)
    
    'V': [],
    'W': [],
    
    'R': [('X', 3), ('T', 4)],
    'X': [],
    'T': [('GG', 2)],
    'GG': [],
    
    'D': [('J', 3)],
    'J': [('Y', 4)],
    'Y': [('Z', 2)],
    'Z': [('AA', 5), ('BB', 3)],
    'AA': [],
    'BB': [],
    
    'E': [('K', 6), ('L', 4)],
    # E->K camino menos óptimo (6), E->L mejor alternativa (4)
    
    'K': [('I', 2)],
    'I': [],
    'L': [('CC', 3)],
    'CC': [('DD', 4), ('EE', 2)],
    # CC->EE más eficiente (2), CC->DD menos óptimo (4)
    
    'DD': [],
    'EE': [('FF', 3)],
    'FF': []
}

camino, costo = ucs(grafo_costo, 'S', 'W')
print("UCS - Camino:", camino, "Costo:", costo)
print("\n" + "="*50)
print("EXPLICACIÓN DE COSTOS ASIGNADOS")
print("="*50)

# Explicación detallada de los costos
explicacion_costos = {
    'S->B (3)': "Camino principal hacia el destino W - más corto y directo",
    'S->E (5)': "Alternativa viable pero no óptima",
    'S->D (6)': "Ruta más larga con menos conexiones útiles",
    'S->A (8)': "Camino más costoso, lleva a rama sin conexión con W",
    'B->H (2)': "Conexión óptima hacia Q y U",
    'B->R (7)': "Desvío significativo, no conduce a W",
    'H->Q (3)': "Camino directo hacia U (que lleva a W)",
    'H->O (5)': "Desvío que no conduce al objetivo",
    'Q->U (4)': "Conexión importante pero con cierto costo de transición",
    'U->W (2)': "Último tramo al destino, costo mínimo",
    'E->L (4)': "Mejor alternativa en rama E",
    'E->K (6)': "Camino menos eficiente en rama E",
    'U->V (6)': "Desvío costoso que no aporta al objetivo"
}

for ruta, explicacion in explicacion_costos.items():
    print(f"{ruta}: {explicacion}")

print("\n" + "="*50)
print("ANÁLISIS DEL CAMINO ÓPTIMO ESPERADO")
print("="*50)
print("Camino esperado: S -> B -> H -> Q -> U -> W")
print("Costo total esperado: 3 + 2 + 3 + 4 + 2 = 14")
print("\nEste camino debería ser seleccionado porque:")
print("1. S->B tiene el costo más bajo desde el inicio")
print("2. B->H es la conexión más eficiente")
print("3. H->Q lleva directamente hacia U")
print("4. Q->U es la única opción hacia el destino")
print("5. U->W tiene el costo mínimo final")