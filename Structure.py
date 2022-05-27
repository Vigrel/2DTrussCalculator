from typing import List, NoReturn, Tuple

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
        self.R  : np.array[List[int]] = np.array(data[7]).astype(int)

        self.elements_list: List[Element] = self.create_elements()
        self.global_stiffness_matrix: List[List[float]] = self.create_global_stiffness_matrix()
        
        data = self.apply_boundary_conditions()
        self.constrained_forces: List[List[float]] = data[0]
        self.constrained_stiffness: List[List[float]] = data[1]
        self.displacement: List[float] = self.get_displacement()
        self.support_reactions: List[float] = self.get_support_reactions()
        self.deformation: List[float] = self.get_deformation()
        self.truss: List[float] = self.get_truss()
        self.internal_forces: List[float] = self.get_internal_forces()

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
    
    def create_global_stiffness_matrix(self) -> List[List[float]]:
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

    def apply_boundary_conditions(self) -> tuple[List[List[float]], List[List[float]]]:
        constrained_forces = np.delete(self.F, self.R, 0)
        constrained_stiffness = np.delete(self.global_stiffness_matrix, self.R, 0)
        constrained_stiffness = np.delete(constrained_stiffness, self.R, 1)

        return (constrained_forces, constrained_stiffness)

    def get_displacement(self) -> List[float]:
        displacement = np.zeros(6)
        counter = 0

        for i in range(len(displacement)):
            if i not in self.R.flatten():
                displacement[i] = np.linalg.solve(self.constrained_stiffness, self.constrained_forces).flatten()[counter]
                counter+=1

        return displacement
    
    def get_support_reactions(self) -> List[float]:
        return np.dot(self.global_stiffness_matrix, self.displacement)[self.R]

    def get_deformation(self) -> List[float]:
        deformations = []

        for element in self.elements_list:
            displacement = [self.displacement[dof - 1] for dof in [element.node1.dofx, element.node1.dofy, element.node2.dofx, element.node2.dofy]]
            deformations.append(
                np.dot([- element.cos, - element.sin, element.cos, element.sin], 
                            displacement) / 
                            element.distance
                            )

        return deformations

    def get_truss(self) -> List[float]:
        return [self.elements_list[element].youngs_module * self.deformation[element] for element in range(self.nm)]

    def get_internal_forces(self) -> List[float]:
        return [self.elements_list[element].area * self.truss[element] for element in range(self.nm)]