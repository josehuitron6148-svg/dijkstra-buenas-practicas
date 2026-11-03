import heapq
from typing import Dict, List, Optional, Tuple


class Grafo:
    """Representa un grafo ponderado para redes de transporte."""

    def __init__(self) -> None:
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def agregar_nodo(self, nodo: str) -> None:
        """Agrega un nodo al grafo si no existe previamente."""
        if nodo not in self.adj:
            self.adj[nodo] = []

    def agregar_arista(
        self,
        origen: str,
        destino: str,
        peso: float,
        bidireccional: bool = True
    ) -> None:
        """Agrega una conexion ponderada entre dos nodos."""
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.adj[origen].append((destino, peso))
        if bidireccional:
            self.adj[destino].append((origen, peso))

    def dijkstra(
        self, origen: str, destino: str
    ) -> Tuple[Optional[float], List[str]]:
        """Calcula la ruta mas corta entre origen y destino."""
        if origen not in self.adj or destino not in self.adj:
            return None, []

        distancias: Dict[str, float] = {
            nodo: float('inf') for nodo in self.adj
        }
        predecesores: Dict[str, Optional[str]] = {
            nodo: None for nodo in self.adj
        }
        distancias[origen] = 0.0

        heap: List[Tuple[float, str]] = [(0.0, origen)]

        while heap:
            dist_actual, nodo_actual = heapq.heappop(heap)

            if nodo_actual == destino:
                break

            if dist_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.adj[nodo_actual]:
                distancia = dist_actual + peso
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(heap, (distancia, vecino))

        if distancias[destino] == float('inf'):
            return None, []

        ruta: List[str] = []
        paso: Optional[str] = destino
        while paso is not None:
            ruta.append(paso)
            paso = predecesores[paso]
        ruta.reverse()

        return distancias[destino], ruta
