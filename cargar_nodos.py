import csv
import os
from typing import List, Tuple

from grafo import Grafo


def cargar_grafo_desde_csv(archivo: str) -> Grafo:
    """Carga los nodos y conexiones desde el CSV instanciando el Grafo."""
    grafo = Grafo()
    if not os.path.exists(archivo):
        return grafo

    with open(archivo, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                origen = fila['origen'].strip()
                destino = fila['destino'].strip()
                peso = float(fila['peso'])
                grafo.agregar_arista(origen, destino, peso)
            except (KeyError, ValueError) as err:
                print(
                    "Advertencia: Fila ignorada por formato "
                    f"invalido ({err})"
                )

    return grafo


def obtener_conexiones_csv(archivo: str) -> List[Tuple[str, str, float]]:
    """Lee y retorna la lista de conexiones almacenadas en el CSV."""
    conexiones: List[Tuple[str, str, float]] = []
    if not os.path.exists(archivo):
        return conexiones

    with open(archivo, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            try:
                origen = fila['origen'].strip()
                destino = fila['destino'].strip()
                peso = float(fila['peso'])
                conexiones.append((origen, destino, peso))
            except (KeyError, ValueError):
                continue
    return conexiones
