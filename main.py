# Título: Ejecución en Consola de Red de Transporte (Proyecto 2)
# Autor: José Isaí Huitrón
# Fecha: 2026-11-16
# Descripción: Interfaz CLI para gestión de grafo en CSV y cálculo Dijkstra.

from io_handler import (
    cargar_grafo_desde_csv,
    guardar_conexion_csv,
    solicitar_datos_conexion,
)

ARCHIVO_CSV = "nodos.csv"


def main() -> None:
    """Punto de entrada principal en modo consola."""
    try:
        grafo = cargar_grafo_desde_csv(ARCHIVO_CSV)
    except FileNotFoundError as err:
        print(f"Aviso: {err} Se iniciará una red vacía.")
        from grafo import Grafo
        grafo = Grafo()

    while True:
        print("\n--- SISTEMA DE RED DE TRANSPORTE (CONSOLA) ---")
        print("1. Registrar nueva conexión")
        print("2. Calcular ruta óptima (Dijkstra)")
        print("3. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            origen, destino, peso = solicitar_datos_conexion()
            guardar_conexion_csv(ARCHIVO_CSV, origen, destino, peso)
            grafo.agregar_arista(origen, destino, peso)
            print(f"Conexión {origen} <-> {destino} guardada.")
        elif opcion == "2":
            origen = input("Nodo de origen: ").strip()
            destino = input("Nodo de destino: ").strip()
            costo, ruta = grafo.dijkstra(origen, destino)
            if costo is None or not ruta:
                print("No existe una ruta válida entre esos nodos.")
            else:
                print(f"Costo mínimo: {costo} | Ruta: {' -> '.join(ruta)}")
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
