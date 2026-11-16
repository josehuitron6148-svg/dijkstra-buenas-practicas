"""

Página web: Red de Transporte (Dijkstra) y Galería Multimedia.

Presentación de poryecto y galería, con un menú lateral de opciones que muestra individualmente
el sistema de cálculo de rutas óptimas y una galería interactiva con
contenido multimedia, modelos 3D y datos del vendedor.

Vendedor_EasyDrive = corporativo o persona a la que se le está proporcionando el uso de la galería.

"""

import csv
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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
    """Inicializa el grafo y la vista activa en la sesión de Streamlit."""
    if "grafo" not in st.session_state:
        st.session_state.grafo = cargar_grafo_desde_csv(ARCHIVO_CSV)
    if "opcion_menu" not in st.session_state:
        st.session_state.opcion_menu = "inicio"


# ==============================================================================
# VISTA 1: SISTEMA DE RED DE TRANSPORTE (DIJKSTRA)
# ==============================================================================

def mostrar_vista_dijkstra() -> None:
    """Renderiza toda la interfaz de gestión de nodos y cálculo de rutas."""
    st.title("🗺️ Sistema de Red de Transporte de Nodos")
    st.markdown("Gestiona conexiones entre nodos y calcula la ruta más corta con **Dijkstra**.")

    col_registro, col_dijkstra = st.columns(2)

    # 1. Agregar nueva conexión
    with col_registro:
        st.subheader("1. Agregar nueva conexión")

        with st.form("form_agregar_conexion", clear_on_submit=True):
            nodo_origen = st.text_input("Nodo de origen", placeholder="Ej. CUGDL").strip()
            nodo_destino = st.text_input("Nodo de destino", placeholder="Ej. CUCEI").strip()
            peso_tramo = st.number_input("Peso / Distancia", min_value=0.0, step=1.0)

            enviado = st.form_submit_button("Guardar conexión", use_container_width=True)

            if enviado:
                if not nodo_origen or not nodo_destino:
                    st.warning("⚠️ Debes ingresar tanto el nodo de origen como el de destino.")
                elif nodo_origen == nodo_destino:
                    st.warning("⚠️ El nodo de origen y destino no pueden ser el mismo.")
                else:
                    guardar_conexion_csv(ARCHIVO_CSV, nodo_origen, nodo_destino, peso_tramo)
                    st.session_state.grafo.agregar_arista(nodo_origen, nodo_destino, peso_tramo)
                    st.success(f"✅ Conexión **{nodo_origen} ↔ {nodo_destino}** ({peso_tramo}) guardada.")
                    st.rerun()

    # 2. Calcular ruta más corta
    with col_dijkstra:
        st.subheader("2. Calcular ruta más corta (Dijkstra)")

        nodos_disponibles = sorted(list(st.session_state.grafo.adj.keys()))

        if not nodos_disponibles:
            st.info("ℹ️ El grafo está vacío. Registra al menos una conexión para calcular rutas.")
        else:
            select_origen = st.selectbox("Selecciona el nodo de origen", nodos_disponibles)
            select_destino = st.selectbox("Selecciona el nodo de destino", nodos_disponibles)

            if st.button("Ejecutar Dijkstra", type="primary", use_container_width=True):
                costo, ruta = st.session_state.grafo.dijkstra(select_origen, select_destino)

                if costo is None or not ruta:
                    st.error(f"❌ No existe una ruta válida entre **{select_origen}** y **{select_destino}**.")
                else:
                    st.success(f"**Costo / Distancia mínima:** {costo}")
                    st.info(f"**Ruta óptima:** {' ➔ '.join(ruta)}")

    st.divider()

    # 3. Visualización de conexiones registradas
    st.subheader("3. Conexiones registradas en la red")

    if os.path.exists(ARCHIVO_CSV) and os.path.getsize(ARCHIVO_CSV) > 0:
        df = pd.read_csv(ARCHIVO_CSV)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.caption(f"Aún no existen conexiones guardadas en '{ARCHIVO_CSV}'.")


# ==============================================================================
# VISTA 2: GALERÍA MULTIMEDIA, MODELOS 3D Y DATOS DEL VENDEDOR
# ==============================================================================

def renderizar_modelo_3d(url_modelo: str, altura: int = 380) -> None:
    """Usarémos un visor 3D interactivo usando (.glb / .gltf)."""
    codigo_html = f"""
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
    <model-viewer
        src="{url_modelo}"
        alt="Modelo 3D Interactivo"
        auto-rotate
        camera-controls
        shadow-intensity="1"
        style="width: 100%; height: {altura}px; background-color: #1e2129; border-radius: 10px;">
    </model-viewer>
    """
    components.html(codigo_html, height=altura + 10)


def mostrar_vista_galeria() -> None:
    """Renderiza una galería estilo catálogo con texto, métricas, imágenes, 3D, video y vendedor."""
    st.title("🖼️ Galería Interactiva y Catálogo")
    st.markdown("Explora recursos visuales, modelos 3D manipulables, demostraciones en video y contacto.")

    # --- BLOQUE 1: INDICADORES NUMÉRICOS (Métricas clave) ---
    st.subheader("📊 Resumen e Indicadores")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Nodos Registrados", value=len(st.session_state.grafo.adj), delta="+Activo")
    m2.metric(label="Modelos 3D", value="2", delta="Interactivos")
    m3.metric(label="Tiempo Promedio Ruta", value="18.5 min", delta="-12%")
    m4.metric(label="Calificación Servicio", value="4.9 / 5.0", delta="Verificado")

    st.divider()

    # --- BLOQUE 2: GALERÍA DE IMÁGENES Y DESCRIPCIONES ---
    st.subheader("📸 Galería Visual")
    col_img1, col_img2, col_img3 = st.columns(3)

    with col_img1:
        st.image(
            "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600",
            caption="Mapeo de Nodos Urbanos",
            use_container_width=True
        )
        st.markdown("**Red Metropolitana:** Visualización geográfica de conexiones intercampus y tramos principales.")

    with col_img2:
        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600",
            caption="Análisis de Distancias",
            use_container_width=True
        )
        st.markdown("**Optimización de Rutas:** Cálculo de pesos mínimos y tiempos estimados de traslado.")

    with col_img3:
        st.image(
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600",
            caption="Infraestructura Tecnológica",
            use_container_width=True
        )
        st.markdown("**Arquitectura Modular:** Procesamiento en tiempo real mediante estructuras de grafos.")

    st.divider()

    # --- BLOQUE 3: MODELOS 3D INTERACTIVOS Y VIDEO ---
    st.subheader("🧊 Modelos 3D Interactivos y Demostración en Video")
    col_3d, col_video = st.columns(2)

    with col_3d:
        st.markdown("**Visor 3D Interactivo** *(Arrastra para rotar, usa la rueda para hacer zoom)*")
        modelo_seleccionado = st.selectbox(
            "Elige un modelo 3D para inspeccionar:",
            options={
                "Astronauta (Prueba 3D)": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
                "Robot Expressive (Prueba 3D)": "https://modelviewer.dev/shared-assets/models/RobotExpressive.glb"
            }.items(),
            format_func=lambda x: x[0]
        )
        renderizar_modelo_3d(modelo_seleccionado[1], altura=360)

    with col_video:
        st.markdown("**Video Demostrativo del Sistema**")
        # Puedes reemplazar esta URL por la ruta de un archivo local ej. "videos/demo.mp4"
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.caption("Demostración operativa del recorrido entre nodos y visualización de datos.")

    st.divider()

    # --- BLOQUE 4: TARJETA CON DATOS DEL VENDEDOR / DESARROLLADOR ---
    st.subheader("👤 Datos del Vendedor / Contacto")
    with st.container(border=True):
        col_avatar, col_info, col_contacto = st.columns([1, 2, 2])

        with col_avatar:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=110)

        with col_info:
            st.markdown("### José Isaí Huitrón")
            st.markdown("**Rol:** Desarrollador & Especialista en Soluciones de Red")
            st.markdown("**Ubicación:** Zapopan, Jalisco, México")
            st.markdown("**Disponibilidad:** Lunes a Viernes, 9:00 AM - 6:00 PM")

        with col_contacto:
            st.markdown("### Información de Contacto")
            st.markdown("📧 **Correo:** contacto.proyecto@ejemplo.com")
            st.markdown("📱 **Teléfono:** +52 (33) 1234-5678")
            st.markdown("🌐 **Repositorio:** `github.com/josehuitron6148-svg`")
            if st.button("Solicitar cotización / información", use_container_width=True):
                st.toast("📩 Solicitud registrada. El vendedor se pondrá en contacto contigo.")


# ==============================================================================
# CONTROLADOR PRINCIPAL (MENÚ DE OPCIONES)
# ==============================================================================

st.set_page_config(
    page_title="Proyecto Programación III",
    page_icon="🧭",
    layout="wide"
)

inicializar_estado()

# Menú lateral con botones de acción explícitos
with st.sidebar:
    st.header("🧭 Menú de Opciones")
    st.markdown("Selecciona el módulo que deseas iniciar:")

    if st.button("🚀 1. Sistema de Rutas (Dijkstra)", use_container_width=True, type="primary"):
        st.session_state.opcion_menu = "dijkstra"

    if st.button("🖼️ 2. Galería 3D y Vendedor", use_container_width=True):
        st.session_state.opcion_menu = "galeria"

    st.divider()
    st.caption("Estado actual: **Activo**")

# Enrutador de vistas según el botón presionado
if st.session_state.opcion_menu == "inicio":
    st.title("Bienvenido al Sistema Integral")
    st.info("👈 Utiliza los **botones del menú lateral** para iniciar el **Sistema de Rutas (Dijkstra)** o explorar la **Galería Multimedia y 3D**.")
elif st.session_state.opcion_menu == "dijkstra":
    mostrar_vista_dijkstra()
elif st.session_state.opcion_menu == "galeria":
    mostrar_vista_galeria()
