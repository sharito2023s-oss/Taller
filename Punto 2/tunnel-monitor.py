import streamlit as st
import pandas as pd
import numpy as np
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import butter, filtfilt
from pathlib import Path
import warnings
import re
warnings.filterwarnings('ignore')

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Análisis de Datos de Sensores - Síndrome del Túnel Carpiano",
    page_icon="🖐️",
    layout="wide"
)

# Título de la aplicación
st.title("🖐️ Sistema de Prevención del Síndrome del Túnel Carpiano")
st.markdown("---")

# Función para limpiar y convertir valores con "V"
def limpiar_valor(valor):
    if isinstance(valor, str):
        # Remover "V" y convertir a float
        valor_limpio = valor.replace('V', '').strip()
        try:
            return float(valor_limpio)
        except:
            return np.nan
    return valor

# Función para cargar y procesar los datos reales
@st.cache_data
def cargar_y_procesar_datos():
    try:
        # Ruta al archivo Excel
        ruta_principal = Path.home() / "Descargas" / "BD_SENSORES.xlsx"
        
        # Verificar si el archivo existe
        if not ruta_principal.exists():
            st.error(f"❌ No se encontró el archivo: {ruta_principal}")
            st.info("Por favor, asegúrate de que el archivo BD_SENSORES.xlsx está en la carpeta Descargas")
            return None
        
        # Cargar datos desde Excel
        st.info(f"📂 Cargando datos desde: {ruta_principal}")
        
        # Leer el archivo Excel - sin encabezados ya que los datos comienzan desde la fila 2
        df_excel = pd.read_excel(ruta_principal, header=None)
        
        # Encontrar la fila donde comienzan los datos numéricos
        fila_inicio = 0
        for i in range(min(10, len(df_excel))):  # Revisar primeras 10 filas
            if any('V' in str(cell) for cell in df_excel.iloc[i] if pd.notna(cell)):
                fila_inicio = i
                break
        
        # Leer nuevamente saltando las filas de encabezado
        df_excel = pd.read_excel(ruta_principal, header=None, skiprows=fila_inicio)
        
        # Limpiar los datos - convertir valores con "V" a números
        for col in df_excel.columns:
            df_excel[col] = df_excel[col].apply(limpiar_valor)
        
        # Eliminar filas completamente vacías
        df_excel = df_excel.dropna(how='all')
        
        # Renombrar columnas
        df_excel.columns = [f'Sensor_{i+1}' for i in range(len(df_excel.columns))]
        
        # Convertir a Polars
        df = pl.from_pandas(df_excel)
        
        st.success(f"✅ Datos cargados exitosamente. Forma: {df.shape}")
        st.info(f"📊 Se detectaron {len(df.columns)} sensores")
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

# Función para aplicar filtros a las señales
def aplicar_filtros(df):
    try:
        # Identificar columnas numéricas
        columnas_numericas = df.select(pl.col(pl.NUMERIC_DTYPES)).columns
        
        if not columnas_numericas:
            st.warning("No se encontraron columnas numéricas para filtrar")
            return df
        
        st.info(f"🔍 Aplicando filtros a {len(columnas_numericas)} señales")
        
        # Diseñar filtro pasa bajas (Butterworth)
        nyquist = 0.5 * 100  # Frecuencia de muestreo asumida de 100 Hz
        normal_cutoff = 5 / nyquist  # Frecuencia de corte de 5 Hz
        b, a = butter(4, normal_cutoff, btype='low', analog=False)
        
        # Aplicar filtro a cada señal
        df_filtrado = df.clone()
        
        for col in columnas_numericas:
            try:
                señal = df[col].to_numpy()
                # Reemplazar NaN si existen
                señal = np.nan_to_num(señal, nan=0.0)
                señal_filtrada = filtfilt(b, a, señal)
                df_filtrado = df_filtrado.with_columns(pl.Series(f"{col}_filtrado", señal_filtrada))
            except Exception as e:
                st.warning(f"No se pudo filtrar la columna {col}: {str(e)}")
        
        return df_filtrado
        
    except Exception as e:
        st.error(f"Error en el filtrado: {str(e)}")
        return df

# Cargar datos
df = cargar_y_procesar_datos()

if df is not None:
    # Mostrar información básica sobre los datos
    st.sidebar.header("Información del Dataset")
    st.sidebar.metric("Muestras", df.shape[0])
    st.sidebar.metric("Sensores", df.shape[1])
    
    # Mostrar primeras filas
    st.subheader("Vista Previa de los Datos (Valores en Voltios)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Mostrar estadísticas básicas
    st.subheader("Estadísticas Descriptivas")
    st.dataframe(df.describe().to_pandas(), use_container_width=True)
    
    # Procesar datos
    df_filtrado = aplicar_filtros(df)
    
    # Sidebar para navegación
    st.sidebar.title("Opciones de Navegación")
    pagina = st.sidebar.radio(
        "Selecciona una sección:",
        ["Visualización de Señales", "Análisis Estadístico", "Datos Filtrados", "Análisis de Frecuencia"]
    )
    
    # Contenido principal según la selección
    if pagina == "Visualización de Señales":
        st.header("📈 Visualización de Señales de Sensores")
        
        # Seleccionar sensor para visualizar
        sensores_disponibles = df.columns
        sensor_seleccionado = st.selectbox(
            "Selecciona un sensor para visualizar:",
            sensores_disponibles
        )
        
        # Crear gráfico de la señal
        st.subheader(f"Señal del {sensor_seleccionado}")
        
        fig = go.Figure()
        
        # Señal original
        fig.add_trace(go.Scatter(
            x=np.arange(len(df)),
            y=df[sensor_seleccionado].to_numpy(),
            name=f"{sensor_seleccionado} (Original)",
            line=dict(color='blue', width=1),
            opacity=0.8
        ))
        
        # Señal filtrada si existe
        columna_filtrada = f"{sensor_seleccionado}_filtrado"
        if columna_filtrada in df_filtrado.columns:
            fig.add_trace(go.Scatter(
                x=np.arange(len(df)),
                y=df_filtrado[columna_filtrada].to_numpy(),
                name=f"{sensor_seleccionado} (Filtrado)",
                line=dict(color='red', width=1.5)
            ))
        
        fig.update_layout(
            title=f"Señal: {sensor_seleccionado}",
            xaxis_title="Muestras",
            yaxis_title="Voltaje (V)",
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Histograma
        st.subheader("📊 Distribución de Valores")
        fig_hist = px.histogram(
            x=df[sensor_seleccionado].to_numpy(),
            title=f"Distribución de {sensor_seleccionado}",
            nbins=50,
            labels={'x': 'Voltaje (V)', 'y': 'Frecuencia'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Box plot
        st.subheader("📦 Diagrama de Caja")
        fig_box = px.box(
            x=df[sensor_seleccionado].to_numpy(),
            title=f"Distribución de {sensor_seleccionado}",
            labels={'x': 'Voltaje (V)'}
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    elif pagina == "Análisis Estadístico":
        st.header("📊 Análisis Estadístico")
        
        # Correlación entre sensores
        st.subheader("🔗 Matriz de Correlación")
        
        try:
            correlacion = df.to_pandas().corr()
            
            fig_corr = px.imshow(
                correlacion,
                title="Matriz de Correlación entre Sensores",
                color_continuous_scale='RdBu_r',
                aspect="auto",
                labels=dict(x="Sensor", y="Sensor", color="Correlación")
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error al calcular correlación: {str(e)}")
        
        # Scatter plot entre dos sensores
        st.subheader("📈 Relación entre Sensores")
        col1, col2 = st.columns(2)
        
        with col1:
            sensor_x = st.selectbox("Sensor X:", df.columns, key="sensor_x")
        with col2:
            sensor_y = st.selectbox("Sensor Y:", df.columns, key="sensor_y")
        
        if sensor_x != sensor_y:
            try:
                fig_scatter = px.scatter(
                    x=df[sensor_x].to_numpy(),
                    y=df[sensor_y].to_numpy(),
                    title=f"{sensor_x} vs {sensor_y}",
                    labels={'x': f'{sensor_x} (V)', 'y': f'{sensor_y} (V)'},
                    trendline="ols"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Calcular correlación
                correlacion = np.corrcoef(df[sensor_x].to_numpy(), df[sensor_y].to_numpy())[0, 1]
                st.metric("Coeficiente de Correlación", f"{correlacion:.3f}")
                
            except Exception as e:
                st.error(f"Error al crear scatter plot: {str(e)}")
    
    elif pagina == "Datos Filtrados":
        st.header("🔧 Datos Filtrados")
        
        # Mostrar columnas filtradas disponibles
        columnas_filtradas = [col for col in df_filtrado.columns if '_filtrado' in col]
        
        if columnas_filtradas:
            st.subheader("Señales Filtradas Disponibles")
            st.write(f"Se aplicaron filtros a {len(columnas_filtradas)} señales")
            
            # Seleccionar sensor para comparar
            sensor_comparar = st.selectbox(
                "Selecciona un sensor para comparar:",
                [col.replace('_filtrado', '') for col in columnas_filtradas]
            )
            
            if f"{sensor_comparar}_filtrado" in df_filtrado.columns:
                # Crear gráfico comparativo
                fig_comp = go.Figure()
                
                # Mostrar solo las primeras 200 muestras para mejor visualización
                n_muestras = min(200, len(df))
                
                # Señal original
                fig_comp.add_trace(go.Scatter(
                    x=np.arange(n_muestras),
                    y=df[sensor_comparar].to_numpy()[:n_muestras],
                    name=f"{sensor_comparar} (Original)",
                    line=dict(color='blue', width=1)
                ))
                
                # Señal filtrada
                fig_comp.add_trace(go.Scatter(
                    x=np.arange(n_muestras),
                    y=df_filtrado[f"{sensor_comparar}_filtrado"].to_numpy()[:n_muestras],
                    name=f"{sensor_comparar} (Filtrado)",
                    line=dict(color='red', width=1.5)
                ))
                
                fig_comp.update_layout(
                    title=f"Comparación: {sensor_comparar} - Original vs Filtrado (primeras {n_muestras} muestras)",
                    xaxis_title="Muestras",
                    yaxis_title="Voltaje (V)",
                    height=500
                )
                
                st.plotly_chart(fig_comp, use_container_width=True)
                
                # Mostrar diferencias
                original = df[sensor_comparar].to_numpy()
                filtrado = df_filtrado[f"{sensor_comparar}_filtrado"].to_numpy()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Media Original", f"{np.mean(original):.3f} V")
                    st.metric("Media Filtrada", f"{np.mean(filtrado):.3f} V")
                with col2:
                    st.metric("Desviación Original", f"{np.std(original):.3f} V")
                    st.metric("Desviación Filtrada", f"{np.std(filtrado):.3f} V")
                with col3:
                    st.metric("Diferencia Media", f"{np.mean(original - filtrado):.3f} V")
        else:
            st.warning("No se aplicaron filtros a ninguna señal")
    
    elif pagina == "Análisis de Frecuencia":
        st.header("📡 Análisis de Frecuencia")
        
        # Seleccionar sensor para análisis espectral
        sensor_analizar = st.selectbox(
            "Selecciona un sensor para análisis de frecuencia:",
            df.columns
        )
        
        señal = df[sensor_analizar].to_numpy()
        señal = np.nan_to_num(señal, nan=0.0)
        
        # Calcular FFT
        fft_señal = np.fft.fft(señal)
        frecuencias = np.fft.fftfreq(len(señal), d=0.01)  # Asumiendo 100Hz de muestreo
        
        # Tomar solo la mitad positiva del espectro
        n = len(señal)
        magnitudes = np.abs(fft_señal[:n//2])
        frecuencias_positivas = frecuencias[:n//2]
        
        # Gráfico de frecuencia
        fig_freq = go.Figure()
        fig_freq.add_trace(go.Scatter(
            x=frecuencias_positivas,
            y=magnitudes,
            name="Espectro de Frecuencia",
            line=dict(color='green', width=1)
        ))
        
        fig_freq.update_layout(
            title=f"Espectro de Frecuencia - {sensor_analizar}",
            xaxis_title="Frecuencia (Hz)",
            yaxis_title="Magnitud",
            height=500
        )
        
        st.plotly_chart(fig_freq, use_container_width=True)
        
        # Encontrar frecuencia dominante
        idx_dominante = np.argmax(magnitudes[1:]) + 1  # Ignorar DC (frecuencia 0)
        freq_dominante = frecuencias_positivas[idx_dominante]
        magnitud_dominante = magnitudes[idx_dominante]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Frecuencia Dominante", f"{abs(freq_dominante):.2f} Hz")
        with col2:
            st.metric("Magnitud Dominante", f"{magnitud_dominante:.2f}")

# Información adicional
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Información del Proyecto:**
    - Tesis: "Diseño de un sistema de prevención del síndrome de túnel carpiano implementando redes neuronales artificiales"
    - Repositorio: [github.com/dialejobv/TESIS_MAESTRIA](https://github.com/dialejobv/TESIS_MAESTRIA)
    - Datos: [github.com/dialejobv/IntroduccionInteligenciaArtificial](https://github.com/dialejobv/IntroduccionInteligenciaArtificial)
    """
)