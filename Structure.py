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

    def create_elements() -> List[Element]:
        pass