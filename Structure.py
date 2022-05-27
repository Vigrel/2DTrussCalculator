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

        self.elements_list: List[Element] = self.create_elements()
        self.global_stiffness_matrix: None = self.create_global_stiffness_matrix()

    def create_elements(self) -> List[Element]:
        elements = []

        for i in range(self.nn):
            ix_n1 = int(self.Inc[i][0])
            node1 = Node(self.N[0][ix_n1 - 1],
                         self.N[1][ix_n1 - 1],
                         ix_n1 * 2 - 1,
                         ix_n1 * 2)

            ix_n2 = int(self.Inc[i][1])
            node2 = Node(self.N[0][ix_n2 - 1],
                         self.N[1][ix_n2 - 1],
                         ix_n2 * 2 - 1,
                         ix_n2 * 2)

            youngs_module = self.Inc[i][2]
            area = self.Inc[i][3]
            
            elements.append(Element(node1, node2, youngs_module, area))
        return elements
    
    def create_global_stiffness_matrix(self) -> None:
        base_matrix = np.zeros((self.nn*2, self.nn*2))

        for element in self.elements_list:
            base_matrix[element.node1.dofx - 1 : element.node1.dofy,
                        element.node1.dofx - 1 : element.node1.dofy] += element.stiffness[:2, :2]
            base_matrix[element.node1.dofx - 1 : element.node1.dofy,
                        element.node2.dofx - 1 : element.node2.dofy] += element.stiffness[2:, :2]
            base_matrix[element.node2.dofx - 1 : element.node2.dofy,
                        element.node1.dofx - 1 : element.node1.dofy] += element.stiffness[:2, 2:]
            base_matrix[element.node2.dofx - 1 : element.node2.dofy,
                        element.node2.dofx - 1 : element.node2.dofy] += element.stiffness[2:, 2:]

        return base_matrix
