class Node:
    """
    A class to represent a Node. In this case, Node is a point on a 2D plane, 
    which connects Element objects.
    ...

    Attributes
    ----------
    x : Node
        Location on the x axis 
    y : Node
        Location on the y axis 
    dofx : float
        Degrees of Freedom on the x axis 
    dofy : float
        Degrees of Freedom on the y axis 
    """
    def __init__(self, x: int, y: int, dofx: int, dofy: int) -> None:
        """
        Constructs all the necessary attributes for the Node object.

        Parameters
        ----------
        x : Node
            Location on the x axis 
        y : Node
            Location on the y axis 
        dofx : float
            Degrees of Freedom on the x axis 
        dofy : float
            Degrees of Freedom on the y axis 
        """

        self.x: int = x
        self.y: int = y
        self.dofx: int = dofx
        self.dofy: int = dofy
