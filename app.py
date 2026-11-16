# Título: Interfaz Web Interactiva con Streamlit - Proyecto 3
# Autor: José Isaí Huitrón
# Fecha: 2026-11-16
# Descripción: Frontend web modular para gestión de redes y galería 3D.

import base64
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from grafo import Grafo
from io_handler import cargar_grafo_desde_csv, guardar_conexion_csv

ARCHIVO_CSV = "nodos.csv"


def inicializar_estado() -> None:
    """Carga el grafo en st.session_state una sola vez por sesión."""
    if "grafo" not in st.session_state:
        try:
            st.session_state.grafo = cargar_grafo_desde_csv(ARCHIVO_CSV)
        except FileNotFoundError:
            st.warning(
                f"Archivo '{ARCHIVO_CSV}' no encontrado. "
                "Se inició un grafo vacío."
            )
            st.session_state.grafo = Grafo()
        except ValueError as err:
            st.error(f"Error de formato en '{ARCHIVO_CSV}': {err}")
            st.session_state.grafo = Grafo()

    if "opcion_menu" not in st.session_state:
        st.session_state.opcion_menu = "inicio"


def renderizar_modelo_3d(ruta_o_url: str, altura: int = 360) -> None:
    """Incrusta un visor 3D interactivo (.glb) desde archivo local o URL."""
    if os.path.exists(ruta_o_url):
        with open(ruta_o_url, "rb") as archivo:
            datos_b64 = base64.b64encode(archivo.read()).decode("utf-8")
        fuente_src = f"data:model/gltf-binary;base64,{datos_b64}"
    else:
        fuente_src = ruta_o_url

    script_visor = (
        "https://ajax.googleapis.com/ajax/libs/model-viewer/"
        "3.4.0/model-viewer.min.js"
    )
    codigo_html = f"""
    <script type="module" src="{script_visor}"></script>
    <model-viewer
        src="{fuente_src}"
        alt="Modelo 3D Interactivo"
        auto-rotate
        camera-controls
        shadow-intensity="1.2"
        exposure="1.1"
        tone-mapping="neutral"
        style="width: 100%; height: {altura}px;
               background-color: #1e2129; border-radius: 10px;">
    </model-viewer>
    """
    components.html(codigo_html, height=altura + 10)


def mostrar_vista_dijkstra() -> None:
    """Renderiza el registro de nodos, cálculo Dijkstra y tabla de red."""
    st.title("🗺️ Sistema de Red de Transporte de Nodos")
    st.markdown(
        "Gestiona conexiones en **nodos.csv** y calcula rutas con "
        "**Dijkstra**."
    )

    col_registro, col_dijkstra = st.columns(2)

    with col_registro:
        st.subheader("1. Agregar nueva conexión")

        with st.form("form_agregar_conexion", clear_on_submit=True):
            nodo_origen = st.text_input(
                "Nodo de origen", placeholder="Ej. CUGDL"
            )
            nodo_destino = st.text_input(
                "Nodo de destino", placeholder="Ej. CUCEI"
            )
            peso_str = st.text_input(
                "Peso / Distancia", placeholder="Ej. 8.5"
            )

            enviado = st.form_submit_button(
                "Guardar conexión", use_container_width=True
            )

            if enviado:
                try:
                    orig_limpio = nodo_origen.strip()
                    dest_limpio = nodo_destino.strip()
                    if not orig_limpio or not dest_limpio:
                        raise ValueError(
                            "Debes ingresar tanto el origen como el destino."
                        )
                    if orig_limpio == dest_limpio:
                        raise ValueError(
                            "El nodo de origen y destino no pueden ser "
                            "iguales."
                        )

                    peso_tramo = float(peso_str)
                    if peso_tramo <= 0:
                        raise ValueError(
                            "El peso debe ser un número mayor a cero."
                        )

                    guardar_conexion_csv(
                        ARCHIVO_CSV, orig_limpio, dest_limpio, peso_tramo
                    )
                    st.session_state.grafo.agregar_arista(
                        orig_limpio, dest_limpio, peso_tramo
                    )
                    st.success(
                        f"✅ Conexión **{orig_limpio} ↔ {dest_limpio}** "
                        f"({peso_tramo}) guardada."
                    )
                    st.rerun()

                except ValueError as err:
                    st.error(f"⚠️ Dato inválido: {err}")
                except PermissionError:
                    st.error(
                        f"❌ Sin permisos para escribir en '{ARCHIVO_CSV}'. "
                        "Ciérralo si está abierto en otro programa."
                    )

    with col_dijkstra:
        st.subheader("2. Calcular ruta más corta (Dijkstra)")

        nodos_disponibles = sorted(list(st.session_state.grafo.adj.keys()))
        if nodos_disponibles:
            st.caption(f"Nodos disponibles: {', '.join(nodos_disponibles)}")

        calc_origen = st.text_input("Ingresa el nodo de origen").strip()
        calc_destino = st.text_input("Ingresa el nodo de destino").strip()

        if st.button(
            "Ejecutar Dijkstra", type="primary", use_container_width=True
        ):
            try:
                if not calc_origen or not calc_destino:
                    raise ValueError(
                        "Debes escribir tanto el nodo origen como el destino."
                    )
                if calc_origen not in st.session_state.grafo.adj:
                    raise KeyError(
                        f"El nodo origen '{calc_origen}' no existe en la red."
                    )
                if calc_destino not in st.session_state.grafo.adj:
                    raise KeyError(
                        f"El nodo destino '{calc_destino}' no existe."
                    )

                costo, ruta = st.session_state.grafo.dijkstra(
                    calc_origen, calc_destino
                )

                if costo is None or not ruta:
                    st.error(
                        f"❌ No existe una ruta válida entre "
                        f"**{calc_origen}** y **{calc_destino}**."
                    )
                else:
                    st.success(f"**Costo / Distancia mínima:** {costo}")
                    st.info(f"**Ruta óptima:** {' ➔ '.join(ruta)}")

            except (ValueError, KeyError) as err:
                st.warning(f"⚠️ {str(err).strip(chr(39))}")

    st.divider()

    st.subheader("3. Conexiones registradas en la red")

    try:
        if not os.path.exists(ARCHIVO_CSV):
            raise FileNotFoundError(
                f"No se encontró el archivo '{ARCHIVO_CSV}'."
            )
        if os.path.getsize(ARCHIVO_CSV) == 0:
            st.caption(f"El archivo '{ARCHIVO_CSV}' está vacío.")
        else:
            df = pd.read_csv(ARCHIVO_CSV)
            st.dataframe(df, use_container_width=True, hide_index=True)
    except FileNotFoundError as err:
        st.warning(str(err))


def mostrar_vista_galeria() -> None:
    """Renderiza galería con métricas, imágenes, 3D, video y vendedor."""
    st.title("🖼️ Galería Interactiva y Catálogo")
    st.markdown(
        "Explora recursos visuales, modelos 3D manipulables, "
        "demostraciones en video y contacto."
    )

    st.subheader("📊 Resumen e Indicadores")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        label="Nodos Registrados",
        value=len(st.session_state.grafo.adj),
        delta="+Activo",
    )
    m2.metric(label="Modelos 3D", value="2", delta="Interactivos")
    m3.metric(label="Tiempo Promedio Ruta", value="18.5 min", delta="-12%")
    m4.metric(
        label="Calificación Servicio", value="4.9 / 5.0", delta="Verificado"
    )

    st.divider()

    st.subheader("📸 Galería Visual")
    col_img1, col_img2, col_img3 = st.columns(3)

    with col_img1:
        st.image(
            "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600",
            caption="Mapeo de Nodos Urbanos",
            use_container_width=True,
        )
        st.markdown(
            "**Red Metropolitana:** Visualización geográfica de conexiones "
            "intercampus y tramos principales."
        )

    with col_img2:
        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600",
            caption="Análisis de Distancias",
            use_container_width=True,
        )
        st.markdown(
            "**Optimización de Rutas:** Cálculo de pesos mínimos y tiempos "
            "estimados de traslado."
        )

    with col_img3:
        st.image(
            "https://images.unsplash.com/"
            "photo-1518770660439-4636190af475?w=600",
            caption="Infraestructura Tecnológica",
            use_container_width=True,
        )
        st.markdown(
            "**Arquitectura Modular:** Procesamiento en tiempo real mediante "
            "estructuras de grafos."
        )

    st.divider()

    st.subheader("🧊 Modelos 3D Interactivos y Demostración en Video")
    col_3d, col_video = st.columns(2)

    with col_3d:
        st.markdown(
            "**Visor 3D Interactivo** *(Arrastra para rotar, usa la rueda "
            "para zoom)*"
        )
        modelo_seleccionado = st.selectbox(
            "Elige un modelo 3D para inspeccionar:",
            options={
                "Vanda Coerulea 3D (Local)": (
                    "modelos/Vanda_coerulea-100k-2048_std_draco.glb"
                ),
                "Astronauta (Prueba 3D)": (
                    "https://modelviewer.dev/shared-assets/models/"
                    "Astronaut.glb"
                ),
            }.items(),
            format_func=lambda x: x[0],
        )
        renderizar_modelo_3d(modelo_seleccionado[1], altura=360)

    with col_video:
        st.markdown("**Video Demostrativo del Sistema**")
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.caption(
            "Demostración operativa del recorrido entre nodos y "
            "visualización de datos."
        )

    st.divider()

    st.subheader("👤 Datos del Vendedor / Contacto")
    with st.container(border=True):
        col_avatar, col_info, col_contacto = st.columns([1, 2, 2])

        with col_avatar:
            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                width=110,
            )

        with col_info:
            st.markdown("### José Isaí Huitrón")
            st.markdown(
                "**Rol:** Desarrollador & Especialista en Soluciones de Red"
            )
            st.markdown("**Ubicación:** Zapopan, Jalisco, México")
            st.markdown(
                "**Disponibilidad:** Lunes a Viernes, 9:00 AM - 6:00 PM"
            )

        with col_contacto:
            st.markdown("### Información de Contacto")
            st.markdown("📧 **Correo:** contacto.proyecto@ejemplo.com")
            st.markdown("📱 **Teléfono:** +52 (33) 1234-5678")
            st.markdown("🌐 **Repositorio:** `github.com/josehuitron6148-svg`")
            if st.button(
                "Solicitar cotización / información",
                use_container_width=True,
            ):
                st.toast(
                    "📩 Solicitud registrada. El vendedor se pondrá en "
                    "contacto contigo."
                )


def main() -> None:
    """Controlador principal de navegación con menú lateral."""
    st.set_page_config(
        page_title="Proyecto Programación III",
        page_icon="🧭",
        layout="wide",
    )

    inicializar_estado()

    with st.sidebar:
        st.header("🧭 Menú de Opciones")
        st.markdown("Selecciona el módulo que deseas iniciar:")

        if st.button(
            "🚀 1. Sistema de Rutas (Dijkstra)",
            use_container_width=True,
            type="primary",
        ):
            st.session_state.opcion_menu = "dijkstra"

        if st.button(
            "🖼️ 2. Galería 3D y Vendedor", use_container_width=True
        ):
            st.session_state.opcion_menu = "galeria"

        st.divider()
        st.caption("Estado actual: **Activo**")

    if st.session_state.opcion_menu == "inicio":
        st.title("Bienvenido al Sistema Integral")
        st.info(
            "👈 Utiliza los **botones del menú lateral** para iniciar el "
            "**Sistema de Rutas (Dijkstra)** o explorar la **Galería "
            "Multimedia y 3D**."
        )
    elif st.session_state.opcion_menu == "dijkstra":
        mostrar_vista_dijkstra()
    elif st.session_state.opcion_menu == "galeria":
        mostrar_vista_galeria()


if __name__ == "__main__":
    main()
