import csv
import os
from typing import Tuple


def guardar_conexion_csv(
    archivo: str, origen: str, destino: str, peso: float
) -> None:
    """Persiste una nueva conexion en el archivo CSV especificado."""
    file_exists = os.path.isfile(archivo)
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
