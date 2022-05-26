from typing import List

import numpy as np

import funcoesTermosol
from Element import Element
from Node import Node

class Structure():
    def __init__(self, file_name: str) -> None:
        data = funcoesTermosol.importa(file_name)
        self.nn: int = data[0]
        self.nm: int = data[2]
        self.nc: int = data[4]
        self.nr: int = data[6]
        self.N  : np.array[List[float]] = np.array(data[1])
        self.Inc: np.array[List[float]] = np.array(data[3])
        self.F  : np.array[List[float]] = np.array(data[5])
        self.R  : np.array[List[float]] = np.array(data[7])

        self.elementos: List[Element] = self.create_elements()

    def create_elements(self) -> List[Element]:
        elementos = []

        for i in range(self.N):
            ix_n1 = int(self.Inc[i][0])
            node1 = Node(self.N[0][ix_n1 - 1],
                         self.N[1][ix_n1 - 1])

            ix_n1 = int(self.Inc[i][1])
            node2 = Node(self.N[0][ix_n1 - 1],
                         self.N[1][ix_n1 - 1])

            youngs_module = self.Inc[i][2]
            area = self.Inc[i][3]
            
            elementos.append(Element(node1, node2, youngs_module, area, i))
        return elementos