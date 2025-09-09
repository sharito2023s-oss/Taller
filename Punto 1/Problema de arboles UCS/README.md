# 🔍 Búsqueda de Costo Uniforme (UCS) - Explicación

## 📋 ¿Qué es UCS?

La Búsqueda de Costo Uniforme (Uniform Cost Search) es un algoritmo que encuentra el camino de menor costo desde un nodo inicial hasta un nodo objetivo en un grafo con aristas ponderadas.

## 🎯 Objetivo del Algoritmo

Encontrar la ruta S → W con el menor costo total en el grafo proporcionado.

## ⚙️ Implementación del Código

```python
def ucs(grafo, inicio, meta):
    cola = [(0, inicio)]  # Cola de prioridad: (costo acumulado, nodo)
    visitados = set()     # Nodos ya procesados
    costo_acumulado = {inicio: 0}  # Mejor costo conocido por nodo
    padre = {inicio: None}  # Para reconstruir el camino
```

Proceso de Búsqueda

```python
while cola:
    costo, nodo = heapq.heappop(cola)  # Saca el nodo con menor costo
    if nodo in visitados:
        continue
    visitados.add(nodo)
    if nodo == meta:  # ¡Meta encontrada!
        break
    # Explora vecinos
    for vecino, costo_arista in grafo[nodo]:
        nuevo_costo = costo + costo_arista
        # Actualiza si encuentra un camino mejor
        if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
            costo_acumulado[vecino] = nuevo_costo
            heapq.heappush(cola, (nuevo_costo, vecino))
            padre[vecino] = nodo
```

## 🗺️ Grafo Analizado

```text
S → A(8), B(3), D(6), E(5)
B → H(2), R(7)
H → O(5), Q(3)
Q → U(4)
U → V(6), W(2)
```
Costos Asignados (Lógica)

- S→B (3): Camino principal - más corto y directo

- S→E (5): Alternativa viable pero no óptima

- S→D (6): Ruta más larga con menos conexiones

- S→A (8): Camino más costoso, sin conexión a W

- B→H (2): Conexión óptima hacia Q y U

- H→Q (3): Camino directo hacia U

- Q→U (4): Conexión importante al camino final

- U→W (2): Último tramo al destino

## 📊 Camino Óptimo Esperado

```text
S --3--> B --2--> H --3--> Q --4--> U --2--> W
```
Cálculo de Costo

```text
3 (S→B) + 2 (B→H) + 3 (H→Q) + 4 (Q→U) + 2 (U→W) = 14
```

## 🎯 ¿Por qué este camino?

- S→B tiene costo 3 - El más bajo desde el inicio

- B→H tiene costo 2 - Conexión más eficiente desde B

- H→Q tiene costo 3 - Única opción que lleva a U

- Q→U tiene costo 4 - Conexión necesaria hacia W

- U→W tiene costo 2 - Tramo final con mínimo costo

## ⚡ Características de UCS

#### ✅ Ventajas

- Óptimo: Siempre encuentra el camino de menor costo

- Completo: Encuentra solución si existe

- Eficiente: Usa cola de prioridad para optimizar búsqueda

#### ⚠️ Consideraciones

- Memoria: Puede consumir mucha memoria en grafos grandes

- Rendimiento: Depende de la estructura del grafo

## 📋 Resultado Esperado

```python
UCS - Camino: ['S', 'B', 'H', 'Q', 'U', 'W']
Costo: 14
```

## 👥 Autores
- **Carlos Andrés Suárez Torres** → [Carlos23Andres](https://github.com/Carlos23Andres)  
- **Saira Sharid Sanabria Muñoz** → [sharito202](https://github.com/sharito202)
