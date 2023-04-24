class Rectangle:
    """
    Rectangle: A class representing a rectangle with dimensions.
    """

    def __init__(self):
        self.x = 0
        self.y = 0

    def dimension(self, dim_x, dim_y):
        """
        Set the dimensions of the rectangle.
        """
        self.x = dim_x
        self.y = dim_y


class Coordinates:
    """
    Coordinates: A class representing a point with x, y, and z coordinates.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def place(self, x, y=0, z=0):
        """
        Set the x, y, and z coordinates of the point.
        """
        self.x = x
        self.y = y
        self.z = z
