# 🔍 Búsqueda en Profundidad (DFS) - Explicación

## 📌 ¿Qué es DFS?

Depth-First Search (Búsqueda en Profundidad) es un algoritmo que explora un grafo hacia lo profundo antes de expandir horizontalmente. Utiliza una estructura LIFO (Last-In, First-Out).

## 🧠 Concepto Clave

"Último en entrar, primero en salir" - Explora completamente una rama antes de pasar a la siguiente.

## 📊 Estructura del Grafo

```python
grafo_costo = {
    'S': [('A', 1), ('B', 1), ('D', 1), ('E', 1)],
    'A': [('F', 1), ('G', 1)],
    'F': [('M', 1)],
    'M': [('N', 1)],
    # ... resto del grafo
}
```

Resultado:
```python
camino, costo = dfs_correcto(grafo_costo, 'S', 'W')
print("DFS - Camino:", camino, "Costo:", costo)
```

## 📊 Paso a Paso de la Búsqueda
1. Inicialización:

- Pila: ['S']

- Visitados: {}

- Padre: {'S': None}

2. Expansión desde S:

- Saca S → Explora vecinos: A, B, D, E

- Pila: ['A', 'B', 'D', 'E'] (orden natural)

- Visitados: {'S'}

- Padres: {'A': 'S', 'B': 'S', 'D': 'S', 'E': 'S'}

3. Continúa con E (último en entrar):

- Saca E → Explora vecinos: K, L

- Pila: ['A', 'B', 'D', 'K', 'L']

- Visitados: {'S', 'E'}

- Padres: {'K': 'E', 'L': 'E'}

4. Sigue profundizando:

- Saca L → Explora CC

- Saca CC → Explora DD, EE

- Saca EE → Explora FF

- ... y así sucesivamente hasta encontrar W

## ⚡ Características de DFS

#### ✅ Ventajas:

- Memoria eficiente: Solo almacena una rama a la vez

- Encuentra soluciones rápidamente si la meta está profunda

- Simple de implementar

####⚠️ Desventajas:

- No garantiza el camino más corto

- Puede entrar en bucles infinitos en grafos cíclicos sin visitados

- Poco eficiente si la meta está cerca pero en rama equivocada

#### 📈 Complejidad:

- Tiempo: O(V + E) - Vértices + Aristas

- Espacio: O(V) - Profundidad máxima de la pila
## 🏗️ Estructura del Algoritmo

```python

pila = [inicio]          # Lista que funciona como pila (LIFO)
visitados = set()        # Conjunto de nodos ya visitados  
padre = {inicio: None}   # Diccionario para reconstruir caminos

```
Flujo del Algoritmo:

- Inicializar con nodo inicial en la pila

- Extraer el último nodo añadido (LIFO)

- Verificar si es el objetivo

- Marcar como visitado

- Explorar vecinos no visitados

- Repetir hasta encontrar meta o agotar opciones

## ⏱️ Complejidad del Algoritmo

- Tiempo: O(V + E) donde V = vértices, E = aristas

- Espacio: O(V) para almacenar nodos visitados

## 👥 Autores
- **Carlos Andrés Suárez Torres** → [Carlos23Andres](https://github.com/Carlos23Andres)  
- **Saira Sharid Sanabria Muñoz** → [sharito202](https://github.com/sharito202)
