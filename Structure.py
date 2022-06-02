from typing import List

import numpy as np

import funcoesTermosol
from Element import Element
from Node import Node


class Structure:
    """
    A class to represent a truss in which all the members lie in a 
    2D plane (planar truss). In this case, a Structure is an arrangement 
    of Element objects connected by Node objects.
    ...

    Attributes
    ----------
    self.nn : int 
        Number of nodes
    self.nm : int
        Number of members
    self.nc : int
        Number of loads
    self.nr : int
        Number of restrictions
    self.N : np.array
        Node coordinates array
    self.Inc : np.array
        Incidence array
    self.F : np.array
        Forces array
    self.R : np.array
        Restrictions array
    self.elements_list : List[Element]
        List of Element objects that compose the Structure object
    self.global_stiffness_matrix : np.array
        Global stiffness matrix of the Structure object
    self.constrained_forces : np.array 
        Global vector of forces
    self.constrained_stiffness : np.array
        Global stiffness matrix of the Structure object 
        after applying boundary conditions
    self.displacement : np.array
        Nodal displacement vector
    self.support_reactions : np.array
        Support reaction forces of the Structure object
    self.deformation : np.array
        Deformation in each member of the Structure object
    self.tensile_forces : np.array
        Internal tensile forces matrix of the Structure object
    self.internal_forces : np.array
        Internal forces matrix of the Structure object

    Methods
    -------
    create_elements():
        Generates the Element objects that compose the Structure, 
        based on the position of the nodes
    create_global_stiffness_matrix():
        Generates the Global stiffness matrix of the Structure object
    apply_boundary_conditions():
        Applies the boundary conditions to the global stiffness matrix
    get_displacement():
        Calculates nodal displacements
    get_support_reactions():
        Calculates the support reaction forces of the Structure object
    get_deformation():
        Calculates the deformation in each member of the Structure object
    get_tensile_forces():
        Calculates the internal tensile forces of the Structure object
    get_internal_forces():
        Calculates the internal forces of the Structure object
    """

    def __init__(self, file_name: str) -> None:
        """
        Constructs all the necessary attributes for the Structure object.

        Parameters
        ----------
        file_name : str
            Name of the file that contains the Structure data
        """

        data = funcoesTermosol.importa(file_name)
        self.nn: int = data[0]
        self.nm: int = data[2]
        self.nc: int = data[4]
        self.nr: int = data[6]
        self.N: np.array = np.array(data[1])
        self.Inc: np.array = np.array(data[3])
        self.F: np.array = np.array(data[5])
        self.R: np.array = np.array(data[7]).astype(int)

        self.elements_list: List[Element] = self.create_elements()
        self.global_stiffness_matrix: np.array = self.create_global_stiffness_matrix()

        data = self.apply_boundary_conditions()
        self.constrained_forces: np.array = data[0]
        self.constrained_stiffness: np.array = data[1]
        self.displacement: np.array = self.get_displacement()
        self.support_reactions: np.array = self.get_support_reactions()
        self.deformation: np.array = self.get_deformation()
        self.tensile_forces: np.array = self.get_tensile_forces()
        self.internal_forces: np.array = self.get_internal_forces()

    def create_elements(self) -> List[Element]:
        """
        Generates the Element objects that compose the Structure, 
        based on the position of the nodes

        Returns
        -------
        elements_list: List[Element]
            List of Element objects that compose the Structure object
        """

        elements = []

        for i in range(self.nm):
            ix_n1 = int(self.Inc[i][0])
            node1 = Node(
                self.N[0][ix_n1 - 1], self.N[1][ix_n1 - 1], ix_n1 * 2 - 1, ix_n1 * 2
            )

            ix_n2 = int(self.Inc[i][1])
            node2 = Node(
                self.N[0][ix_n2 - 1], self.N[1][ix_n2 - 1], ix_n2 * 2 - 1, ix_n2 * 2
            )

            youngs_module = self.Inc[i][2]
            area = self.Inc[i][3]

            elements.append(Element(node1, node2, youngs_module, area))
        return elements

    def create_global_stiffness_matrix(self) -> np.array:
        """
        Generates the Global stiffness matrix of the Structure object

        Returns
        -------
        global_stiffness_matrix : np.array
            Global stiffness matrix of the Structure object
        """

        base_matrix = np.zeros((self.nn * 2, self.nn * 2))

        for element in self.elements_list:
            base_matrix[
                element.node1.dofx - 1 : element.node1.dofy,
                element.node1.dofx - 1 : element.node1.dofy,
            ] += element.stiffness[:2, :2]
            base_matrix[
                element.node2.dofx - 1 : element.node2.dofy,
                element.node1.dofx - 1 : element.node1.dofy,
            ] += element.stiffness[2:, :2]
            base_matrix[
                element.node1.dofx - 1 : element.node1.dofy,
                element.node2.dofx - 1 : element.node2.dofy,
            ] += element.stiffness[:2, 2:]
            base_matrix[
                element.node2.dofx - 1 : element.node2.dofy,
                element.node2.dofx - 1 : element.node2.dofy,
            ] += element.stiffness[2:, 2:]

        return base_matrix

    def apply_boundary_conditions(self) -> tuple[np.array, np.array]:
        """
        Applies the boundary conditions to the global stiffness matrix

        Returns
        -------
        constrained_forces : np.array 
            Global vector of forces
        constrained_stiffness : np.array
            Global stiffness matrix of the Structure object after applying 
            boundary conditions
        """
        constrained_forces = np.delete(self.F, self.R, 0)
        constrained_stiffness = np.delete(self.global_stiffness_matrix, self.R, 0)
        constrained_stiffness = np.delete(constrained_stiffness, self.R, 1)

        return (constrained_forces, constrained_stiffness)

    def get_displacement(self) -> np.array:
        """
        Calculates nodal displacements

        Returns
        -------
        displacement : np.array
            Nodal displacement vector
        """
        
        counter = 0
        displacement = np.linalg.solve(
            self.constrained_stiffness, self.constrained_forces
        )
        complete_displacement = np.zeros(self.nn*2)

        for i in range(len(complete_displacement)):
            if i not in self.R.flatten():
                complete_displacement[i] = displacement[counter]
                counter+=1

        return complete_displacement

    def get_support_reactions(self) -> np.array:
        """
        Calculates the support reaction forces of the Structure object

        Returns
        -------
        support_reactions : np.array
            Support reaction forces of the Structure object
        """

        return np.dot(self.global_stiffness_matrix, self.displacement)[self.R]

    def get_deformation(self) -> np.array:
        """
        Calculates the deformation in each member of the Structure object

        Returns
        -------
        deformation : np.array
            Deformation in each member of the Structure object
        """

        deformations = []

        for element in self.elements_list:
            displacement = [
                self.displacement[dof - 1]
                for dof in [
                    element.node1.dofx,
                    element.node1.dofy,
                    element.node2.dofx,
                    element.node2.dofy,
                ]
            ]
            deformations.append(
                np.dot(
                    [-element.cos, -element.sin, element.cos, element.sin], displacement
                )
                / element.distance
            )

        return deformations

    def get_tensile_forces(self) -> np.array:
        """
        Calculates the internal tensile forces of the Structure object

        Returns
        -------
        tensile_forces : np.array
            Internal tensile forces matrix of the Structure object
        """

        return [
            self.elements_list[element].youngs_module * self.deformation[element]
            for element in range(self.nm)
        ]

    def get_internal_forces(self) -> np.array:
        """
        Calculates the internal forces of the Structure object

        Returns
        -------
        internal_forces : np.array
            Internal forces matrix of the Structure object
        """

        return [
            self.elements_list[element].area * self.tensile_forces[element]
            for element in range(self.nm)
        ]
