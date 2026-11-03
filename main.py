import os

from cargar_nodos import cargar_grafo_desde_csv
from io_handler import (
    guardar_conexion_csv,
    solicitar_datos_conexion
)

ARCHIVO_CSV = 'nodo.csv'


def mostrar_menu() -> None:
    """Despliega el menu de opciones del sistema."""
    print("\n" + "=" * 42)
    print("  SISTEMA DE RED DE TRANSPORTE DE NODOS")
    print("=" * 42)
    print("1. Agregar nueva conexion")
    print("2. Calcular ruta mas corta (Dijkstra)")
    print("3. Mostrar conexiones registradas")
    print("4. Salir")
    print("=" * 42)


def ejecutar_dijkstra() -> None:
    """Ejecuta la busqueda del camino minimo usando Dijkstra."""
    grafo = cargar_grafo_desde_csv(ARCHIVO_CSV)
    if not grafo.adj:
        print("\nEl grafo esta vacio. Ingrese conexiones primero.")
        return

    nodos = list(grafo.adj.keys())
    print(f"\nNodos disponibles en la red: {', '.join(nodos)}")

    origen = input("Ingrese el nodo de origen: ").strip()
    destino = input("Ingrese el nodo de destino: ").strip()

    costo, ruta = grafo.dijkstra(origen, destino)

    if costo is None:
        msg = (
            f"\nNo existe una ruta valida entre "
            f"'{origen}' y '{destino}'."
        )
        print(msg)
    else:
        print(f"\nCosto/Distancia total mas corta: {costo}")
        print(f"Ruta optima: {' -> '.join(ruta)}")


def listar_conexiones() -> None:
    """Muestra en pantalla el listado de conexiones guardadas."""
    if not os.path.exists(ARCHIVO_CSV):
        print("\nNo se encontro el archivo de datos 'nodo.csv'.")
        return

    grafo = cargar_grafo_desde_csv(ARCHIVO_CSV)
    print("\n--- Conexiones Activas en el Grafo ---")
    impresas = 0
    for origen, vecinos in grafo.adj.items():
        for destino, peso in vecinos:
            print(f"{origen} <--> {destino} [Peso: {peso}]")
            impresas += 1

    if impresas == 0:
        print("No existen conexiones registradas.")


def main() -> None:
    """Menu interactivo principal."""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion (1-4): ").strip()

        if opcion == "1":
            origen, destino, peso = solicitar_datos_conexion()
            guardar_conexion_csv(ARCHIVO_CSV, origen, destino, peso)
            print(
                f"\nExito: Conexion {origen} -> {destino} "
                f"({peso}) guardada."
            )
        elif opcion == "2":
            ejecutar_dijkstra()
        elif opcion == "3":
            listar_conexiones()
        elif opcion == "4":
            print("\nPrograma finalizado correctamente.")
            break
        else:
            print("\nOpcion no valida. Intente de nuevo.")


if __name__ == '__main__':
    main()
