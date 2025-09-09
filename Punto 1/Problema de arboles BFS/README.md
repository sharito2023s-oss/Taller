# 🔍 Búsqueda en Amplitud (BFS) - Explicación

## 📌 ¿Qué es BFS?

Breadth-First Search (Búsqueda en Amplitud) es un algoritmo que explora todos los nodos de un grafo nivel por nivel, comenzando desde el nodo inicial y expandiéndose hacia sus vecinos antes de profundizar.

## 🎯 Objetivo del Algoritmo

- Encontrar el camino más corto (en términos de número de aristas) desde el nodo inicial 'S' hasta el nodo objetivo 'W'.

## 📊 Estructura del Grafo

```python
graph = {
    'S': ['A','B','D','E'],
    'A': ['F','G'],
    'B': ['H','R'],
    # ... más nodos
}
```
## ⚙️ Implementación BFS

```python
from collections import deque

def bfs(graph, start, goal):
    visited = set()  # Nodos ya explorados
    queue = deque([[start]])  # Cola con caminos a explorar

    if start == goal:
        return "Start and goal nodes are the same"

    while queue:
        path = queue.popleft()  # Tomar el primer camino de la cola
        node = path[-1]  # Último nodo del camino

        if node not in visited:
            neighbors = graph[node]  # Obtener vecinos del nodo actual

            for neighbor in neighbors:
                new_path = list(path)  # Copiar el camino actual
                new_path.append(neighbor)  # Agregar el vecino
                queue.append(new_path)  # Añadir nuevo camino a la cola

                if neighbor == goal:
                    return new_path  # ¡Meta encontrada!

            visited.add(node)  # Marcar nodo como visitado

    return "No path found"
```

Este código implementa el algoritmo de búsqueda en amplitud (BFS) para encontrar la ruta más corta entre dos nodos en un grafo.

#### 🎯 Funcionamiento General:

El programa funciona como un explorador metódico que va visitando todos los puntos conectados nivel por nivel. Imagina que estás en una red de ciudades conectadas por carreteras y quieres encontrar el camino con menos paradas desde tu ciudad inicial hasta tu destino.

#### 📋 Proceso Paso a Paso:

- Comienza desde el nodo de inicio ('S') y lo marca como punto de partida

- Explora sistemáticamente todos los vecinos directos primero

- Luego pasa a los vecinos de esos vecinos, y así sucesivamente

- Lleva registro de todos los caminos posibles que va descubriendo

- Cuando encuentra el nodo objetivo ('W'), inmediatamente devuelve el camino completo

- Si agota todas las posibilidades sin encontrar el objetivo, indica que no hay ruta

#### ⚡ Característica Clave:

La clave de BFS es que siempre encuentra el camino más corto en términos de número de pasos, porque explora todos los caminos del nivel actual antes de pasar al siguiente nivel.

## 🔄 Proceso de Ejecución

Paso a Paso:

1. Inicio: queue = [['S']], visited = {}

2. Expandir S: Vecinos = ['A','B','D','E']

    - Nuevos caminos: ['S','A'], ['S','B'], ['S','D'], ['S','E']

3. Expandir A: Vecinos = ['F','G']

    - Nuevos caminos: ['S','A','F'], ['S','A','G']

4. Expandir B: Vecinos = ['H','R']

    - Nuevos caminos: ['S','B','H'], ['S','B','R']

5. Continue expandiendo nivel por nivel hasta encontrar 'W'

## 📈 Visualización del Camino

Camino Encontrado:

```text
S → B → H → Q → U → W
```
Explicación del Resultado:

- S: Nodo inicial

- B: Primer vecino expandido

- H: Vecino de B

- Q: Vecino de H

- U: Vecino de Q

- W: Vecino de U → ¡Objetivo encontrado!

## ⏱️ Complejidad del Algoritmo

- Tiempo: O(V + E) donde V = vértices, E = aristas

- Espacio: O(V) para almacenar nodos visitados

## 👥 Autores
- **Carlos Andrés Suárez Torres** → [Carlos23Andres](https://github.com/Carlos23Andres)  
- **Saira Sharid Sanabria Muñoz** → [sharito202](https://github.com/sharito202)
