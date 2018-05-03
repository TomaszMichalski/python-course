#Object representations of all possible shapes.

#Point
#Defined by providing numerical values of x and y coordinates
#Color is optional
class Point: 
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y

#Polygon
#Defined by providing list of Points.
#Color is optional
class Polygon:
    def __init__(self, points, color=None):
        self.points = points

#Rectangle
#Defined by providing Point representing center of the shape
#and it's width and height
#Color is optional
class Rectangle:
    def __init__(self, center, width, height, color=None):
        self.center = center
        self.width = width
        self.height = height

#Square
#Defined by providing Point representing center of the shape and it's size
#Color is optional
class Square:
    def __init__(self, center, size, color=None):
        self.center = center
        self.size = size

#Circle
#Defined by providing Point representing center of the shape and it's radius
#Color is optional
class Circle:
    def __init__(self, center, radius, color=None):
        self.center = center
        self.size = size