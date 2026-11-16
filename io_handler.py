# Título: Manejador de Persistencia y Entrada/Salida (CSV)
# Autor: José Isaí Huitrón
# Fecha: 2026-11-16
# Descripción: Lectura, escritura y validación de nodos y aristas en CSV.

import csv
import os
from typing import Tuple

from grafo import Grafo


def cargar_grafo_desde_csv(archivo: str) -> Grafo:
    """Lee un archivo CSV y construye una instancia de Grafo."""
    grafo = Grafo()
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"No se encontró el archivo '{archivo}'.")

    if os.path.getsize(archivo) == 0:
        return grafo

    with open(archivo, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames or not {
            "origen", "destino", "peso"
        }.issubset(lector.fieldnames):
            raise ValueError(
                "El CSV debe tener las columnas: origen,destino,peso"
            )

        for fila in lector:
            origen = fila["origen"].strip()
            destino = fila["destino"].strip()
            peso = float(fila["peso"])
            grafo.agregar_arista(origen, destino, peso)

    return grafo


def guardar_conexion_csv(
    archivo: str, origen: str, destino: str, peso: float
) -> None:
    """Persiste una nueva conexion en el archivo CSV especificado."""
    file_exists = os.path.isfile(archivo) and os.path.getsize(archivo) > 0
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['origen', 'destino', 'peso'])
        writer.writerow([origen, destino, peso])


def solicitar_datos_conexion() -> Tuple[str, str, float]:
    """Solicita y valida interactivamente los datos de la conexion."""
    while True:
        try:
            origen = input("Ingrese el nodo de origen: ").strip()
            if not origen:
                raise ValueError("El nodo de origen no puede estar vacio.")

            destino = input("Ingrese el nodo de destino: ").strip()
            if not destino:
                raise ValueError("El nodo de destino no puede estar vacio.")

            if origen == destino:
                msg = "El nodo de origen y destino no pueden ser iguales."
                raise ValueError(msg)

            peso_str = input("Ingrese el peso (distancia/tiempo): ").strip()
            peso = float(peso_str)
            if peso <= 0:
                msg = "El peso debe ser un valor numerico positivo mayor a 0."
                raise ValueError(msg)

            return origen, destino, peso
        except ValueError as err:
            print(f"Error de entrada: {err}. Intente nuevamente.\n")
