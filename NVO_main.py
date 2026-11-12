"""Sistema de Red de Transporte de Nodos (Interfaz Web con Streamlit).

Combina la gestión de persistencia en CSV, visualización tabular y el cálculo
de rutas óptimas mediante el algoritmo de Dijkstra en un único punto de entrada.
"""

import csv
import os

import pandas as pd
import streamlit as st

from grafo import Grafo

# Constantes de configuración
ARCHIVO_CSV = "conexiones.csv"
COLUMNAS_CSV = ["origen", "destino", "peso"]


# ==============================================================================
# CAPA DE PERSISTENCIA (Manejo de CSV y carga del Grafo)
# ==============================================================================

def cargar_grafo_desde_csv(ruta_archivo: str) -> Grafo:
    """Construye y retorna una instancia de Grafo a partir de un archivo CSV."""
    grafo = Grafo()
    if not os.path.exists(ruta_archivo) or os.path.getsize(ruta_archivo) == 0:
        return grafo

    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            origen = fila["origen"].strip()
            destino = fila["destino"].strip()
            peso = float(fila["peso"])
            grafo.agregar_arista(origen, destino, peso)

    return grafo


def guardar_conexion_csv(ruta_archivo: str, origen: str, destino: str, peso: float) -> None:
    """Guarda una nueva conexión en el archivo CSV creando encabezados si no existen."""
    archivo_tiene_datos = os.path.exists(ruta_archivo) and os.path.getsize(ruta_archivo) > 0

    with open(ruta_archivo, mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_CSV)
        if not archivo_tiene_datos:
            escritor.writeheader()
        escritor.writerow({
            "origen": origen,
            "destino": destino,
            "peso": peso
        })


def inicializar_estado() -> None:
    """Carga el grafo en la sesión de Streamlit una sola vez al iniciar."""
    if "grafo" not in st.session_state:
        st.session_state.grafo = cargar_grafo_desde_csv(ARCHIVO_CSV)


# ==============================================================================
# INTERFAZ DE USUARIO (Streamlit)
# ==============================================================================

st.set_page_config(
    page_title="Sistema de Red de Transporte",
    page_icon="🗺️",
    layout="wide"
)

inicializar_estado()

st.title(" Sistema de Red de Transporte de Nodos")
st.markdown("Gestiona conexiones entre nodos y calcula la ruta más corta con **Dijkstra**.")

# Dividimos la pantalla en dos columnas principales para mejor ergonomía visual
col_registro, col_dijkstra = st.columns(2)

# ------------------------------------------------------------------------------
# SECCIÓN 1: AGREGAR NUEVA CONEXIÓN (Columna Izquierda)
# ------------------------------------------------------------------------------
with col_registro:
    st.subheader("1. Agregar nueva conexión")

    with st.form("form_agregar_conexion", clear_on_submit=True):
        nodo_origen = st.text_input("Nodo de origen", placeholder="Ej. A").strip()
        nodo_destino = st.text_input("Nodo de destino", placeholder="Ej. B").strip()
        peso_tramo = st.number_input("Peso / Distancia", min_value=0.0, step=1.0)

        enviado = st.form_submit_button("Guardar conexión", use_container_width=True)

        if enviado:
            if not nodo_origen or not nodo_destino:
                st.warning(" Debes ingresar tanto el nodo de origen como el de destino.")
            elif nodo_origen == nodo_destino:
                st.warning(" El nodo de origen y destino no pueden ser el mismo.")
            else:
                guardar_conexion_csv(ARCHIVO_CSV, nodo_origen, nodo_destino, peso_tramo)
                st.session_state.grafo.agregar_arista(nodo_origen, nodo_destino, peso_tramo)
                st.success(f" Conexión **{nodo_origen} ↔ {nodo_destino}** ({peso_tramo}) guardada.")
                st.rerun()

# ------------------------------------------------------------------------------
# SECCIÓN 2: CALCULAR RUTA MÁS CORTA - DIJKSTRA (Columna Derecha)
# ------------------------------------------------------------------------------
with col_dijkstra:
    st.subheader("2. Calcular ruta más corta (Dijkstra)")

    # Obtenemos los nodos disponibles directamente del grafo (como en tu código CLI)
    nodos_disponibles = sorted(list(st.session_state.grafo.adj.keys()))

    if not nodos_disponibles:
        st.info("ℹ El grafo está vacío. Registra al menos una conexión para calcular rutas.")
    else:
        # Usar selectbox evita errores de dedo al escribir nombres de nodos
        select_origen = st.selectbox("Selecciona el nodo de origen", nodos_disponibles)
        select_destino = st.selectbox("Selecciona el nodo de destino", nodos_disponibles)

        if st.button("Ejecutar Dijkstra", type="primary", use_container_width=True):
            costo, ruta = st.session_state.grafo.dijkstra(select_origen, select_destino)

            if costo is None or not ruta:
                st.error(f" No existe una ruta válida entre **{select_origen}** y **{select_destino}**.")
            else:
                st.success(f"**Costo / Distancia mínima:** {costo}")
                st.info(f"**Ruta óptima:** {' ➔ '.join(ruta)}")

st.divider()

# ------------------------------------------------------------------------------
# SECCIÓN 3: VISUALIZACIÓN DE CONEXIONES REGISTRADAS (Ancho completo)
# ------------------------------------------------------------------------------
st.subheader("3. Conexiones registradas en la red")

if os.path.exists(ARCHIVO_CSV) and os.path.getsize(ARCHIVO_CSV) > 0:
    df = pd.read_csv(ARCHIVO_CSV)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.caption("Aún no existen conexiones guardadas en 'nodo.csv'.")
