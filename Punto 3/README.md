# 🤖 Navegación de Agente con Campos Potenciales

## 📋 Descripción General

Este proyecto implementa un agente inteligente basado en el algoritmo de Campos Potenciales para resolver el laberinto mostrado en la práctica.
El objetivo del agente es desplazarse desde el punto inicial (🔴 círculo rojo en la esquina inferior izquierda) hasta la meta (✅ estrella verde en la esquina superior derecha), evitando colisiones con obstáculos y bordes.

- La técnica de Campos Potenciales combina fuerzas:

- Campo atractivo hacia el objetivo.

- Campo repulsivo de los obstáculos.

- Campo repulsivo de bordes para no salirse del área.

- Campo para evitar ciclos y movimientos repetitivos.

Además, el agente incluye mecanismos para detectar estancamientos u oscilaciones, y cuenta con un modo de escape que permite buscar rutas alternativas si queda atrapado.

## 🧩 Problema a Resolver

- Entrada: Un entorno tipo laberinto definido por bloques de obstáculos y bordes.

- Salida: Una trayectoria válida desde el inicio hasta el objetivo.

- Restricciones:

    - No atravesar obstáculos.

    - No salir de los límites del entorno.

    - Evitar ciclos y quedarse estancado.


## ⚙️ Implementación

1. Definición del Entorno

- Inicio: (1.0, 1.0)

- Objetivo: (26.0, 14.0)

- Obstáculos: Representados como bloques rectangulares convertidos en puntos individuales.

- Bordes: Limitan el área a 0 ≤ x ≤ 27 y 0 ≤ y ≤ 15.

2. Parámetros del Algoritmo

- K_ATRACTIVO = 1.5 → Intensidad del campo hacia la meta.

- K_REPULSIVO = 30000.0 → Intensidad de repulsión contra obstáculos.

- K_BORDES = 15000.0 → Intensidad de repulsión contra bordes.

- RADIO_REPULSION = 2.5 → Distancia de influencia de los obstáculos.

- PASO = 0.25 → Tamaño de cada movimiento del agente.

- UMBRAL_CONVERGENCIA = 0.5 → Cercanía mínima al objetivo para considerar que fue alcanzado.

3. Funcionalidades del Agente

✅ Atractivo hacia el objetivo

✅ Repulsión de obstáculos y bordes

✅ Memoria de posiciones visitadas para evitar ciclos

✅ Detección de estancamiento y oscilaciones

✅ Modo escape con búsqueda alternativa de rutas

✅ Visualización en tiempo real de la trayectoria y estado

## 🎥 Visualización y Animación

![Captura desde 2025-09-09 22-54-27](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%203/Captura%20desde%202025-09-09%2022-54-27.png?raw=true)

Se utiliza Matplotlib para mostrar:

- Obstáculos (⬛ grises).

- Punto de inicio (🔴).

- Objetivo (⭐ verde).

- Trayectoria recorrida (🔵 línea).

- Estado del agente (normal, escape, estancado, oscilando).

Al llegar al objetivo, aparece el mensaje "¡OBJETIVO ALCANZADO!".

## 📊 Resultados Esperados

- El agente logra desplazarse desde el inicio hasta el objetivo.

- Se genera una trayectoria fluida y optimizada que evita colisiones.

- Se muestran estadísticas:

- Iteraciones realizadas.

- Distancia final al objetivo.

- Cantidad de posiciones visitadas.

- Estado final (objetivo alcanzado o no).

## 👥 Autores
- **Carlos Andrés Suárez Torres** → [Carlos23Andres](https://github.com/Carlos23Andres)  
- **Saira Sharid Sanabria Muñoz** → [sharito202](https://github.com/sharito202)

