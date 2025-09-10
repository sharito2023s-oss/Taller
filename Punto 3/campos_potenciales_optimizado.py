import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import time
from collections import deque

# =============================================================================
# CONFIGURACIÓN INICIAL DEL ENTORNO Y POSICIONES
# =============================================================================

# Posición inicial del agente (representado por 'o')
agente_posicion = np.array([1.0, 1.0])

# Posición del objetivo (representado por '*')
objetivo = np.array([26.0, 14.0])

# Definición de obstáculos como bloques sólidos (coordenadas de los rectángulos)
# Cada bloque se define como [x_inicio, y_inicio, ancho, alto]
bloques_obstaculos = [
    # Primera línea horizontal superior (convertida a bloque)
    [9, 13, 10, 2],  # [x, y, ancho, alto] - cubre de [9,13] a [18,14]
    
    # Bloque izquierdo superior
    [2, 11, 5, 2],   # [2,11] a [6,12]
    
    # Extensión vertical del bloque izquierdo
    [5, 8, 2, 3],    # [5,8] a [6,10]
    
    # Bloque central grande
    [2, 6, 10, 2],   # [2,6] a [11,7]
    
    # Columnas verticales izquierdas
    [5, 2, 2, 4],    # [5,2] a [6,5]
    
    # Columnas verticales centrales
    [10, 1, 2, 5],   # [10,1] a [11,5]
    
    # Estructura en forma de T invertida
    [8, 10, 2, 2],   # [8,10] to [9,11]
    [8, 9, 4, 2],    # [8,9] to [11,10] - adjusted to connect
    
    # Estructura compleja derecha - parte superior
    [17, 10, 2, 3],  # [17,10] to [18,12]
    
    # Estructura compleja derecha - parte media
    [14, 8, 5, 2],   # [14,8] to [18,9]
    [18, 6, 1, 2],   # [18,6] to [18,7] - individual column
    
    # Estructura compleja derecha - parte inferior
    [14, 4, 5, 2],   # [14,4] to [18,5]
    [14, 1, 2, 2],   # [14,1] to [15,2]
    
    # Estructura final en el extremo derecho - parte superior
    [20, 11, 3, 3],  # [20,11] to [22,13]
    
    # Estructura final en extremo derecho - parte media
    [22, 9, 2, 2],   # [23,9] to [24,10]
    [21, 7, 2, 2],   # [21,7] to [22,8]
    
    # Estructura final en extremo derecho - parte inferior
    [21, 5, 6, 2],   # [21,5] to [26,6]
    [20, 2, 2, 2],   # [20,2] to [21,3]
]

# Convertir bloques a puntos individuales para la lógica de colisiones
obstaculos = []
for bloque in bloques_obstaculos:
    x, y, ancho, alto = bloque
    for i in range(int(ancho)):
        for j in range(int(alto)):
            obstaculos.append([x + i, y + j])

obstaculos = np.array(obstaculos, dtype=float)

# =============================================================================
# PARÁMETROS DEL ALGORITMO DE CAMPOS POTENCIALES - OPTIMIZADOS
# =============================================================================

# Constantes para los campos potenciales (OPTIMIZADAS PARA ESTE ENTORNO)
K_ATRACTIVO = 1.5        # Constante para el campo atractivo (AUMENTADO)
K_REPULSIVO = 30000.0    # Constante para el campo repulsivo de obstáculos (AJUSTADO)
K_BORDES = 15000.0       # Constante para el campo repulsivo de bordes (AJUSTADO)
RADIO_REPULSION = 2.5    # Radio de influencia de los obstáculos (AUMENTADO)
RADIO_BORDES = 2.5       # Radio de influencia de los bordes
PASO = 0.25              # Tamaño del paso de movimiento (AUMENTADO)
UMBRAL_CONVERGENCIA = 0.5  # Distancia mínima para considerar que llegó al objetivo

# =============================================================================
# CLASE DEL AGENTE INTELIGENTE CON NAVEGACIÓN MEJORADA
# =============================================================================

class AgenteCamposPotenciales:
    def __init__(self, posicion_inicial, objetivo, obstaculos):
        self.posicion = np.array(posicion_inicial, dtype=float)
        self.objetivo = np.array(objetivo, dtype=float)
        self.obstaculos = np.array(obstaculos, dtype=float)
        
        # Historial para detección de estancamiento y oscilaciones
        self.historial_posiciones = [self.posicion.copy()]
        self.estancado = False
        self.oscilando = False
        self.contador_estancamiento = 0
        self.contador_oscilaciones = 0
        self.max_estancamiento = 8
        self.max_oscilaciones = 10
        
        # Para visualización
        self.trayectoria = [self.posicion.copy()]
        self.modo_escape = False
        self.iteraciones_escape = 0
        self.max_iteraciones_escape = 20
        
        # Memoria de posiciones visitadas para evitar ciclos
        self.posiciones_visitadas = set()
        self.agregar_posicion_visitada(self.posicion)
        
    def agregar_posicion_visitada(self, posicion):
        """Agrega una posición discretizada al conjunto de posiciones visitadas"""
        # Discretizamos la posición para evitar duplicados por pequeñas diferencias
        pos_discreta = (round(posicion[0], 1), round(posicion[1], 1))
        self.posiciones_visitadas.add(pos_discreta)
        
    def ha_visitado_cercano(self, posicion, umbral=0.5):
        """Verifica si una posición cercana ya ha sido visitada"""
        for pos_visitada in self.posiciones_visitadas:
            if np.linalg.norm(posicion - np.array(pos_visitada)) < umbral:
                return True
        return False
        
    def calcular_campo_atractivo(self):
        """Calcula el campo atractivo hacia el objetivo"""
        direccion = self.objetivo - self.posicion
        distancia = np.linalg.norm(direccion)
        
        if distancia < 0.1:
            return np.zeros(2)
            
        # Campo atractivo proporcional a la distancia (más fuerte cerca del objetivo)
        factor = 1.0 + 5.0 / (distancia + 1.0)  # Más fuerza cuando está cerca del objetivo
        return K_ATRACTIVO * factor * direccion
    
    def calcular_campo_repulsivo_obstaculos(self):
        """Calcula el campo repulsivo de los obstáculos"""
        fuerza_repulsiva = np.zeros(2)
        
        for obstaculo in self.obstaculos:
            direccion = self.posicion - obstaculo
            distancia = np.linalg.norm(direccion)
            
            if distancia < RADIO_REPULSION:
                # Solo considerar obstáculos dentro del radio de repulsión
                if distancia < 0.1:
                    distancia = 0.1
                    
                # Fuerza repulsiva inversamente proporcional a la distancia
                factor = (1.0/distancia - 1.0/RADIO_REPULSION)
                magnitud = K_REPULSIVO * factor * factor
                fuerza_repulsiva += magnitud * (direccion / distancia)
                
        return fuerza_repulsiva
    
    def calcular_campo_repulsivo_bordes(self):
        """Calcula el campo repulsivo de los bordes del circuito"""
        fuerza_repulsiva = np.zeros(2)
        
        # Bordes del circuito
        dist_izquierdo = self.posicion[0]
        dist_derecho = 27 - self.posicion[0]
        dist_inferior = self.posicion[1]
        dist_superior = 15 - self.posicion[1]
        
        # Fuerza desde bordes izquierdo y derecho
        if dist_izquierdo < RADIO_BORDES:
            factor = (1.0/dist_izquierdo - 1.0/RADIO_BORDES)
            magnitud = K_BORDES * factor * factor
            fuerza_repulsiva[0] += magnitud
            
        if dist_derecho < RADIO_BORDES:
            factor = (1.0/dist_derecho - 1.0/RADIO_BORDES)
            magnitud = K_BORDES * factor * factor
            fuerza_repulsiva[0] -= magnitud
            
        # Fuerza desde bordes inferior y superior
        if dist_inferior < RADIO_BORDES:
            factor = (1.0/dist_inferior - 1.0/RADIO_BORDES)
            magnitud = K_BORDES * factor * factor
            fuerza_repulsiva[1] += magnitud
            
        if dist_superior < RADIO_BORDES:
            factor = (1.0/dist_superior - 1.0/RADIO_BORDES)
            magnitud = K_BORDES * factor * factor
            fuerza_repulsiva[1] -= magnitud
                
        return fuerza_repulsiva
    
    def calcular_campo_evitar_ciclos(self):
        """Campo repulsivo para evitar volver a posiciones ya visitadas"""
        fuerza_repulsiva = np.zeros(2)
        umbral_deteccion = 1.5  # Radio para detectar posiciones visitadas
        
        for pos_visitada in self.posiciones_visitadas:
            pos_array = np.array([pos_visitada[0], pos_visitada[1]])
            direccion = self.posicion - pos_array
            distancia = np.linalg.norm(direccion)
            
            if distancia < umbral_deteccion and distancia > 0.1:
                # Fuerza repulsiva para evitar ciclos
                factor = (1.0/distancia - 1.0/umbral_deteccion)
                magnitud = 8000.0 * factor * factor
                fuerza_repulsiva += magnitud * (direccion / distancia)
                
        return fuerza_repulsiva
    
    def detectar_estancamiento(self):
        """Detecta si el agente está estancado"""
        if len(self.historial_posiciones) < 10:
            return False
            
        # Calcular distancia recorrida en las últimas 10 iteraciones
        posiciones_recientes = self.historial_posiciones[-10:]
        desplazamiento_total = 0
        
        for i in range(1, len(posiciones_recientes)):
            desplazamiento_total += np.linalg.norm(posiciones_recientes[i] - posiciones_recientes[i-1])
            
        if desplazamiento_total < 1.0:  # Menos estricto
            self.contador_estancamiento += 1
            if self.contador_estancamiento >= self.max_estancamiento:
                return True
        else:
            self.contador_estancamiento = max(0, self.contador_estancamiento - 1)
            
        return False
    
    def detectar_oscilaciones(self):
        """Detecta si el agente está oscilando entre posiciones"""
        if len(self.historial_posiciones) < 15:
            return False
            
        # Calcular si está yendo hacia atrás en la dirección del objetivo
        direccion_objetivo = self.objetivo - self.posicion
        if len(self.historial_posiciones) > 1:
            direccion_movimiento = self.posicion - self.historial_posiciones[-2]
            producto_punto = np.dot(direccion_objetivo, direccion_movimiento)
            
            if producto_punto < 0:  # Se está moviendo away from objetivo
                self.contador_oscilaciones += 1
            else:
                self.contador_oscilaciones = max(0, self.contador_oscilaciones - 1)
                
        if self.contador_oscilaciones >= self.max_oscilaciones:
            return True
            
        return False
    
    def buscar_ruta_alternativa(self):
        """Busca una ruta alternativa cuando está estancado u oscilando"""
        self.modo_escape = True
        self.iteraciones_escape = 0
        
        # Intentar encontrar una dirección que lleve hacia el objetivo pero evite obstáculos
        direccion_objetivo = self.objetivo - self.posicion
        direccion_objetivo = direccion_objetivo / np.linalg.norm(direccion_objetivo)
        
        # Generar varias direcciones alternativas alrededor de la dirección al objetivo
        mejores_direcciones = []
        for angulo in np.linspace(-np.pi/2, np.pi/2, 12):  # Probar 12 direcciones diferentes
            # Rotar la dirección hacia el objetivo
            cos_ang = np.cos(angulo)
            sin_ang = np.sin(angulo)
            direccion_rotada = np.array([
                direccion_objetivo[0] * cos_ang - direccion_objetivo[1] * sin_ang,
                direccion_objetivo[0] * sin_ang + direccion_objetivo[1] * cos_ang
            ])
            
            # Verificar si esta dirección es prometedora
            pos_futura = self.posicion + direccion_rotada * PASO * 3
            if not self.verificar_colision(pos_futura) and not self.ha_visitado_cercano(pos_futura):
                # Calcular qué tan buena es esta dirección (más cerca del objetivo es mejor)
                distancia_actual = np.linalg.norm(self.objetivo - self.posicion)
                distancia_futura = np.linalg.norm(self.objetivo - pos_futura)
                mejora = distancia_actual - distancia_futura
                mejores_direcciones.append((mejora, direccion_rotada))
        
        # Elegir la mejor dirección
        if mejores_direcciones:
            mejores_direcciones.sort(reverse=True, key=lambda x: x[0])
            return mejores_direcciones[0][1] * PASO * 2.0
        
        # Si no hay buenas direcciones, usar una aleatoria
        angulo = np.random.rand() * 2 * np.pi
        return np.array([np.cos(angulo), np.sin(angulo)]) * PASO * 2.0
    
    def mover_en_modo_escape(self):
        """Movimiento especial cuando está en modo de escape"""
        self.iteraciones_escape += 1
        
        if self.iteraciones_escape >= self.max_iteraciones_escape:
            self.modo_escape = False
            self.estancado = False
            self.oscilando = False
            self.contador_estancamiento = 0
            self.contador_oscilaciones = 0
            return self.mover()
        
        return self.buscar_ruta_alternativa()
    
    def verificar_colision(self, posicion):
        """Verifica colisiones con obstáculos y bordes"""
        # Verificar colisiones con obstáculos
        for obstaculo in self.obstaculos:
            if np.linalg.norm(posicion - obstaculo) < 0.7:  # Radio de colisión
                return True
                
        # Verificar colisiones con bordes
        if (posicion[0] < 0.5 or posicion[0] > 26.5 or 
            posicion[1] < 0.5 or posicion[1] > 14.5):
            return True
            
        return False
    
    def mover(self):
        """Realiza un movimiento del agente"""
        distancia_al_objetivo = np.linalg.norm(self.objetivo - self.posicion)
        if distancia_al_objetivo < UMBRAL_CONVERGENCIA:
            return False
        
        if self.modo_escape:
            movimiento = self.mover_en_modo_escape()
        else:
            self.estancado = self.detectar_estancamiento()
            self.oscilando = self.detectar_oscilaciones()
            
            if self.estancado or self.oscilando:
                movimiento = self.buscar_ruta_alternativa()
            else:
                # Calcular todas las fuerzas
                fuerza_atractiva = self.calcular_campo_atractivo()
                fuerza_repulsiva_obstaculos = self.calcular_campo_repulsivo_obstaculos()
                fuerza_repulsiva_bordes = self.calcular_campo_repulsivo_bordes()
                fuerza_evitar_ciclos = self.calcular_campo_evitar_ciclos()  # Para evitar ciclos
                
                # Combinar fuerzas
                fuerza_total = (fuerza_atractiva + 
                               fuerza_repulsiva_obstaculos + 
                               fuerza_repulsiva_bordes +
                               fuerza_evitar_ciclos)
                
                # Normalizar y aplicar paso
                norma = np.linalg.norm(fuerza_total)
                if norma > 0:
                    movimiento = (fuerza_total / norma) * PASO
                else:
                    # Movimiento aleatorio si no hay fuerza
                    angulo = np.random.rand() * 2 * np.pi
                    movimiento = np.array([np.cos(angulo), np.sin(angulo)]) * PASO * 0.5
        
        # Aplicar movimiento con verificación de colisiones
        nueva_posicion = self.posicion + movimiento
        
        # Verificar colisión y ajustar si es necesario
        if self.verificar_colision(nueva_posicion):
            # Intentar reducir el movimiento
            movimiento_reducido = movimiento * 0.5
            nueva_posicion = self.posicion + movimiento_reducido
            
            if self.verificar_colision(nueva_posicion):
                # Si todavía hay colisión, buscar dirección alternativa
                angulo = np.random.rand() * 2 * np.pi
                movimiento = np.array([np.cos(angulo), np.sin(angulo)]) * PASO * 0.5
                nueva_posicion = self.posicion + movimiento
                
                # Si sigue habiendo colisión, quedarse en el mismo lugar
                if self.verificar_colision(nueva_posicion):
                    nueva_posicion = self.posicion.copy()
        
        # Asegurar que está dentro de los límites
        nueva_posicion[0] = np.clip(nueva_posicion[0], 0.5, 26.5)
        nueva_posicion[1] = np.clip(nueva_posicion[1], 0.5, 14.5)
        
        # Actualizar posición
        self.posicion = nueva_posicion
        self.historial_posiciones.append(self.posicion.copy())
        self.agregar_posicion_visitada(self.posicion)
        
        # Mantener el historial manejable
        if len(self.historial_posiciones) > 100:
            self.historial_posiciones.pop(0)
            
        self.trayectoria.append(self.posicion.copy())
        
        return True

# =============================================================================
# VISUALIZACIÓN Y ANIMACIÓN
# =============================================================================

# Crear figura
fig, ax = plt.subplots(figsize=(14, 10))

# Crear agente
agente = AgenteCamposPotenciales(agente_posicion, objetivo, obstaculos)

# Función de inicialización
def init():
    ax.clear()
    
    # Dibujar obstáculos como bloques sólidos
    for bloque in bloques_obstaculos:
        x, y, ancho, alto = bloque
        rect = patches.Rectangle((x-0.5, y-0.5), ancho, alto, 
                                linewidth=1, edgecolor='darkgray', 
                                facecolor='gray', alpha=0.7)
        ax.add_patch(rect)

    # Dibujar objetivo
    ax.scatter(objetivo[0], objetivo[1], color='lime', marker='*', s=400, 
                edgecolors='darkgreen', linewidth=2, zorder=5, label='Objetivo')

    # Dibujar punto de inicio
    ax.scatter(agente_posicion[0], agente_posicion[1], color='red', s=200, 
                edgecolors='darkred', linewidth=2, zorder=5, label='Punto inicial')

    # Dibujar bordes
    ax.plot([0, 27], [15, 15], 'k-', linewidth=4)
    ax.plot([27, 27], [15, 0], 'k-', linewidth=4)
    ax.plot([27, 0], [0, 0], 'k-', linewidth=4)
    ax.plot([0, 0], [0, 15], 'k-', linewidth=4)

    # Configuración
    ax.set_xlim(-0.5, 27.5)
    ax.set_ylim(-0.5, 15.5)
    ax.set_aspect('equal')
    ax.set_title("Navegación por Campos Potenciales - Ruta Optimizada", 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Coordenada X", fontsize=12)
    ax.set_ylabel("Coordenada Y", fontsize=12)
    ax.grid(True, alpha=0.4, linestyle='--')
    ax.legend(loc="upper left", fontsize=11, framealpha=0.9)
    
    return ax,

# Función de actualización
def update(frame):
    continuar = agente.mover()
    
    ax.clear()
    
    # Dibujar elementos estáticos
    for bloque in bloques_obstaculos:
        x, y, ancho, alto = bloque
        rect = patches.Rectangle((x-0.5, y-0.5), ancho, alto, 
                                linewidth=1, edgecolor='darkgray', 
                                facecolor='gray', alpha=0.7)
        ax.add_patch(rect)
    
    ax.scatter(objetivo[0], objetivo[1], color='lime', marker='*', s=400, 
                edgecolors='darkgreen', linewidth=2, zorder=5, label='Objetivo')
    ax.scatter(agente_posicion[0], agente_posicion[1], color='red', s=200, 
                edgecolors='darkred', linewidth=2, zorder=5, label='Punto inicial')
    
    # Dibujar bordes
    ax.plot([0, 27], [15, 15], 'k-', linewidth=4)
    ax.plot([27, 27], [15, 0], 'k-', linewidth=4)
    ax.plot([27, 0], [0, 0], 'k-', linewidth=4)
    ax.plot([0, 0], [0, 15], 'k-', linewidth=4)
    
    # Dibujar trayectoria
    if len(agente.trayectoria) > 1:
        trayectoria_arr = np.array(agente.trayectoria)
        ax.plot(trayectoria_arr[:, 0], trayectoria_arr[:, 1], 'b-', alpha=0.6, linewidth=2, label='Trayectoria')
    
    # Dibujar agente
    color_agente = 'orange' if agente.modo_escape else 'blue'
    ax.scatter(agente.posicion[0], agente.posicion[1], color=color_agente, s=150, 
               edgecolors='darkblue', linewidth=2, zorder=6, label='Agente')
    
    # Información de estado
    distancia = np.linalg.norm(agente.objetivo - agente.posicion)
    estado = "Normal"
    if agente.modo_escape:
        estado = "Modo Escape"
    elif agente.estancado:
        estado = "Estancado"
    elif agente.oscilando:
        estado = "Oscilando"
        
    info_text = f"Iteración: {frame}\nDistancia al objetivo: {distancia:.2f}\n"
    info_text += f"Estado: {estado}\n"
    info_text += f"Posiciones visitadas: {len(agente.posiciones_visitadas)}"
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Configuración
    ax.set_xlim(-0.5, 27.5)
    ax.set_ylim(-0.5, 15.5)
    ax.set_aspect('equal')
    ax.set_title("Navegación por Campos Potenciales - Ruta Optimizada")
    ax.set_xlabel("Coordenada X")
    ax.set_ylabel("Coordenada Y")
    ax.grid(True, alpha=0.4, linestyle='--')
    ax.legend(loc="upper left")
    
    if not continuar:
        ax.text(0.5, 0.5, "¡OBJETIVO ALCANZADO!", transform=ax.transAxes, fontsize=20,
                ha='center', va='center', bbox=dict(boxstyle='round', facecolor='lime', alpha=0.8))
        ani.event_source.stop()
    
    return ax,

# Crear animación
ani = FuncAnimation(fig, update, frames=5000, init_func=init, interval=100, repeat=False)

plt.tight_layout()
plt.show()

# Visualización final
fig_final, ax_final = plt.subplots(figsize=(14, 10))

for bloque in bloques_obstaculos:
    x, y, ancho, alto = bloque
    rect = patches.Rectangle((x-0.5, y-0.5), ancho, alto, 
                            linewidth=1, edgecolor='darkgray', 
                            facecolor='gray', alpha=0.7)
    ax_final.add_patch(rect)

ax_final.scatter(objetivo[0], objetivo[1], color='lime', marker='*', s=400, 
                edgecolors='darkgreen', linewidth=2, zorder=5, label='Objetivo')
ax_final.scatter(agente_posicion[0], agente_posicion[1], color='red', s=200, 
                edgecolors='darkred', linewidth=2, zorder=5, label='Punto inicial')

# Bordes
ax_final.plot([0, 27], [15, 15], 'k-', linewidth=4)
ax_final.plot([27, 27], [15, 0], 'k-', linewidth=4)
ax_final.plot([27, 0], [0, 0], 'k-', linewidth=4)
ax_final.plot([0, 0], [0, 15], 'k-', linewidth=4)

# Trayectoria
if len(agente.trayectoria) > 1:
    trayectoria_arr = np.array(agente.trayectoria)
    ax_final.plot(trayectoria_arr[:, 0], trayectoria_arr[:, 1], 'b-', alpha=0.6, linewidth=2, label='Trayectoria')
    ax_final.scatter(agente.posicion[0], agente.posicion[1], color='blue', s=150, 
                   edgecolors='darkblue', linewidth=2, zorder=6, label='Posición final')

# Configuración final
ax_final.set_xlim(-0.5, 27.5)
ax_final.set_ylim(-0.5, 15.5)
ax_final.set_aspect('equal')
ax_final.set_title("Trayectoria Final - Navegación por Campos Potenciales", fontsize=16, fontweight='bold')
ax_final.set_xlabel("Coordenada X", fontsize=12)
ax_final.set_ylabel("Coordenada Y", fontsize=12)
ax_final.grid(True, alpha=0.4, linestyle='--')
ax_final.legend(loc="upper left", fontsize=11, framealpha=0.9)

# Resultado
distancia_final = np.linalg.norm(agente.objetivo - agente.posicion)
resultado_texto = f"Distancia final al objetivo: {distancia_final:.2f}\n"
resultado_texto += f"Posiciones visitadas: {len(agente.posiciones_visitadas)}"
if distancia_final < UMBRAL_CONVERGENCIA:
    resultado_texto += "\n¡OBJETIVO ALCANZADO!"
else:
    resultado_texto += "\nObjetivo no alcanzado"

ax_final.text(0.5, 0.02, resultado_texto, transform=ax_final.transAxes, fontsize=12,
             ha='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.show()