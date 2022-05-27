from typing import List

import numpy as np

from Node import Node

class Element():
    def __init__(self, node1: Node, node2: Node, youngs_module: float, area: float) -> None:
        self.node1: Node = node1
        self.node2: Node = node2
        self.youngs_module: float = youngs_module
        self.area: float = area

        self.distance: float = ((self.node2.x - self.node1.x)**2 + (self.node2.y - self.node1.y)**2)**0.5

        self.stiffness: np.ndarray[List[float]] = self.calculate_stiffness()

    def calculate_stiffness(self) -> List[List[float]]:
        sin = (self.node2.y - self.node1.y) / self.distance
        cos = (self.node2.x - self.node1.x) / self.distance

        cos2 = cos**2
        sin2 = sin**2
        sico = cos*sin

        matriz = np.array([
            [ cos2, sico , -cos2, -sico],
            [ sico, sin2 , -sico, -sin2],
            [-cos2, -sico, cos2 , sico ],
            [-sico, -sin2, sico , sin2 ]
        ])

        K = self.area*self.youngs_module/self.distance
   
        return np.multiply(K, matriz)
