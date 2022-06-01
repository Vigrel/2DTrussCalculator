from typing import List

import numpy as np

from Node import Node


class Element:
    """
    A class to represent an Element. In this case, an Element is a planar truss.
    ...

    Attributes
    ----------
    node1 : Node
        First node of the truss
    node2 : Node
        Second node of the truss
    youngs_module : float
        Young's module of the truss material
    area : float
        Cross-sectional area of the truss
    self.distance : float
        Distance between the two nodes of the truss
    stiffness : np.ndarray[List[float]]
        Stiffness array of the truss
    sin : float
        Sin of the angle between the truss and the x-axis
    cos : float
        Cos of the angle between the truss and the x-axis

    Methods
    -------
    calculate_stiffness():
        Calculates the stiffness matrix of the truss element
    """

    def __init__(
        self, node1: Node, node2: Node, youngs_module: float, area: float
    ) -> None:
        """
        Constructs all the necessary attributes for the Element object.

        Parameters
        ----------
        node1 : Node
            First node of the truss
        node2 : Node
            Second node of the truss
        youngs_module : float
            Young's module of the truss material
        area : float
            Cross-sectional area of the truss
        """

        self.node1: Node = node1
        self.node2: Node = node2
        self.youngs_module: float = youngs_module
        self.area: float = area

        self.distance: float = (
            (self.node2.x - self.node1.x) ** 2 + (self.node2.y - self.node1.y) ** 2
        ) ** 0.5

        self.stiffness: np.ndarray[List[float]] = self.calculate_stiffness()

    def calculate_stiffness(self) -> List[List[float]]:
        """
        Calculates the stiffness matrix of the truss element.

        Returns
        -------
        stiffness : np.ndarray[List[float]]
            Stiffness array of the truss element
        """

        self.sin = (self.node2.y - self.node1.y) / self.distance
        self.cos = (self.node2.x - self.node1.x) / self.distance

        cos2 = self.cos**2
        sin2 = self.sin**2
        sico = self.cos * self.sin

        matriz = np.array(
            [
                [cos2, sico, -cos2, -sico],
                [sico, sin2, -sico, -sin2],
                [-cos2, -sico, cos2, sico],
                [-sico, -sin2, sico, sin2],
            ]
        )

        K = self.area * self.youngs_module / self.distance

        return np.multiply(K, matriz)
