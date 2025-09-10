# 🖐️ Sistema de Prevención del Síndrome del Túnel Carpiano

## 📋 Descripción del Proyecto

Este proyecto es un dashboard interactivo desarrollado en Streamlit para el análisis de datos de sensores relacionados con la prevención del síndrome del túnel carpiano. El sistema procesa, visualiza y analiza datos de sensores EMG y otros sensores biomédicos para identificar patrones y características relevantes.

## 🎯 Objetivo

Desarrollar un sistema de análisis de datos que permita:

- Procesar datos crudos de sensores biomédicos

- Aplicar técnicas de filtrado y preprocesamiento

- Visualizar señales y características relevantes

- Identificar patrones asociados al síndrome del túnel carpiano

## 🛠️ Librerias Utilizadas

- Streamlit - Dashboard interactivo

- Polars - Procesamiento eficiente de datos

- Plotly - Visualizaciones interactivas

- Scipy - Procesamiento de señales digitales

- Pandas - Manipulación de datos

- NumPy - Cálculos numéricos

## 📊 Estructura del Dataset

El dataset BD_SENSORES.xlsx contiene:

- Formato: Valores en voltios (ej: "1.66V", "0.32V")

- Sensores: 61 canales de datos EMG/sensores (Sensor_1 a Sensor_61)

- Muestras: 30 muestras temporales de actividad muscular

- Origen: Datos reales de la tesis de maestría sobre prevención del síndrome del túnel carpiano

## 🎨 Vizualizacion en Streamlit

![Streamlit](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%202/Streamlit.png?raw=true)

### 📊 1. Visualización de Señales

Señal Temporal Original vs Filtrada


¿Qué muestra?

- Línea azul: Señal original del sensor en el dominio del tiempo

- Línea roja: Señal filtrada (suavizada) después del procesamiento

- Eje X: Número de muestras (25 muestras mostradas)

- Eje Y: Voltaje en voltios (V) - representa la actividad muscular

Interpretación: El filtrado suaviza la señal eliminando ruido 
mientras preserva la información relevante de la actividad muscular.

Histograma de Distribución

![Histograma de Distribución](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%202/Histograma%20de%20Distribución.png?raw=true)

Qué muestra?

- Distribución de los valores de voltaje del Sensor_2

- Eje X: Rango de voltajes (0-0.4V)

- Eje Y: Frecuencia de ocurrencia de cada valor

Interpretación: La mayoría de las mediciones del Sensor_2 se concentran alrededor de 0.1-0.2V, indicando un rango típico de actividad.

Diagrama de Caja

![Diagrama de Caja](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%202/Diagrama%20de%20Caja.png?raw=true)

¿Qué muestra?

- Caja central: Rango intercuartílico (25%-75% de los datos)

- Línea media: Mediana de los datos

- Bigotes: Rango completo de los datos (excluyendo outliers)

- Puntos: Valores atípicos (outliers)

Interpretación: El Sensor_2 muestra una distribución concentrada con mediana alrededor de 0.15V y pocos valores atípicos.

### 📈 2. Análisis Estadístico

Matriz de Correlación

![Matriz de Correlación](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%202/Matriz%20de%20Correlación.png?raw=true)

¿Qué muestra?

- Correlaciones entre los 61 sensores

- Colores cálidos (rojos): Correlación positiva fuerte

- Colores fríos (azules): Correlación negativa fuerte

- Blanco/colores neutros: Poca o ninguna correlación

Interpretación: Los sensores muestran patrones de correlación que pueden indicar grupos musculares que se activan de manera coordinada.

### 🔧 3. Datos Filtrados

Comparación Original vs Filtrado

![Comparación Original vs Filtrado](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%202/Comparación%20Original%20vs%20Filtrado.png?raw=true)

¿Qué muestra?

- Comparación detallada entre señal original y filtrada

- Métricas cuantitativas:

    - Media original: 1.439V vs Media filtrada: 1.438V

    - Desviación estándar: 0.031V en ambos casos

    - Diferencia media: 0.000V (minima alteración)

Interpretación: El filtrado preserva perfectamente las características estadísticas principales mientras elimina el ruido.

📡 4. Análisis de Frecuencia
Espectro de Frecuencia

![Espectro de Frecuencia](https://github.com/Sharito2023s-oss/Taller/blob/main/Punto%202/Espectro%20de%20Frecuencia.png?raw=true)

¿Qué muestra?

- Espectro de frecuencia de la señal del Sensor_4

- Eje X: Frecuencia en Hertz (Hz)

- Eje Y: Magnitud de cada componente frecuencial

- Pico dominante: 3.33Hz con magnitud 8.06

Interpretación: La actividad muscular principal del Sensor_4 ocurre alrededor de 3.33Hz, lo que podría corresponder a la frecuencia natural de contracción muscular.

## 🔧 Funciones Principales
cargar_y_procesar_datos()

- Carga el archivo Excel desde la carpeta de Descargas

- Detecta automáticamente el inicio de los datos numéricos

- Convierte valores con formato "V" a números flotantes

- Limpia y prepara los datos para análisis

aplicar_filtros(df)

- Aplica filtros Butterworth pasa-bajos (5Hz cut-off) a las señales

- Maneja valores NaN y outliers

- Genera versiones filtradas de todas las señales

Visualizaciones

- Gráficos interactivos con Plotly

- Selección dinámica de sensores

- Comparaciones entre datos originales y filtrados

- Análisis temporal y frecuencial

