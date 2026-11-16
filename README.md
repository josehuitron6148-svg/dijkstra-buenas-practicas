
"""
# Taller de Buenas Prácticas - Programación III

**Autor:** José Carlos Isaí Huitrón Barrón
**Fecha de creación:** 13 de octubre del 2026
**Descripción:** Taller de buenas prácticas para la clase de programación III.

---

## Descripción del Proyecto
# Sistema de Red de Transporte (Dijkstra) y Galería Interactiva 3D

Aplicación modular en Python que implementa el **Algoritmo de Dijkstra** para el cálculo de rutas óptimas en redes de transporte (centros universitarios UdeG), combinando una interfaz web interactiva construida con **Streamlit**, persistencia en CSV y una galería multimedia con modelos 3D manipulables.

---

## Características Principales

* **Cálculo de Rutas Óptimas (Dijkstra):** Determina el camino de menor costo o distancia entre dos nodos registrados en la red[cite: 4, 13, 18].
* **Persistencia Desacoplada en CSV:** Lectura, validación y registro de conexiones mediante el archivo `nodos.csv` (`origen,destino,peso`)[cite: 15, 16].
* **Interfaz Web Interactiva (`app.py`):** Menú lateral de navegación con gestión de estado (`st.session_state`), validación de entradas y manejo de excepciones específicas (`FileNotFoundError`, `ValueError`, `KeyError`, `PermissionError`)[cite: 13].
* **Galería Multimedia y Visor 3D:** Visualización de indicadores clave, catálogo visual, video demostrativo y visor 3D interactivo (`model-viewer`) compatible con archivos `.glb` locales[cite: 13].
* **Ejecución en Consola (`main.py`):** Conserva la interfaz CLI original para operar el sistema desde terminal.
* **Calidad de Código:** Cumple con la guía de estilo **PEP 8** validada mediante **Flake8**[cite: 17].

---

## Estructura del Proyecto

```text
dijkstra-buenas-practicas/
├── app.py                  # Interfaz web principal con Streamlit y galería 3D
├── main.py                 # Interfaz de línea de comandos (CLI)
├── grafo.py                # Estructura de datos Grafo y algoritmo de Dijkstra
├── io_handler.py           # Capa de persistencia y validación de archivos CSV
├── nodos.csv               # Base de datos de conexiones (origen,destino,peso)
├── modelos/                # Recursos 3D locales (.glb)
│   └── Vanda_coerulea-100k-2048_std_draco.glb
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación técnica
