#Object representations of all possible shapes.

figure_types = ["point", "polygon", "rectangle", "square", "circle"]

#Point
#Defined by providing numerical values of x and y coordinates
#Color is optional
class Point: 
    def __init__(self, x, y, color=None):
        self.x = float(x)
        self.y = float(y)
        self.color = color

    def __str__(self):
        if self.color == None:
            return "Point [x=" + str(self.x) + ",y=" + str(self.y) + "]"
        return "Point [x=" + str(self.x) + ",y=" + str(self.y) + ",color=" + self.color + "]"

#Polygon
#Defined by providing list of Points.
#Color is optional
class Polygon:
    def __init__(self, points, color=None):
        self.points = []
        for point in points:
            self.points.append(Point(point[0], point[1]))
        self.color = color

    def __str__(self):
        out = "Polygon ["
        for point in self.points:
            out += "[x=" + str(point.x) + ",y=" + str(point.y) + "],"
        out = out[:-1]
        out += "]"
        if self.color != None:
            out += ",color=" + self.color + "]"
        return out

#Rectangle
#Defined by providing Point representing center of the shape
#and it's width and height
#Color is optional
class Rectangle:
    def __init__(self, center, width, height, color=None):
        self.center = center
        center.x = float(center.x)
        center.y = float(center.y)
        self.width = float(width)
        self.height = float(height)
        self.color = color

    def __str__(self):
        if self.color == None:
            return "Rectangle [x=" + str(self.x()) + ",y=" + str(self.y()) + ",width=" + str(self.width) + ",heigth=" + str(self.height) + "]"
        return "Rectangle [x=" + str(self.x()) + ",y=" + str(self.y()) + ",width=" + str(self.width) + ",heigth=" + str(self.height) + ",color=" + self.color + "]"

    def x(self):
        return self.center.x

    def y(self):
        return self.center.y

#Square
#Defined by providing Point representing center of the shape and it's size
#Color is optional
class Square:
    def __init__(self, center, size, color=None):
        self.center = center
        center.x = float(center.x)
        center.y = float(center.y)
        self.size = float(size)
        self.color = color

    def __str__(self):
        if self.color == None:
            return "Square [x=" + str(self.x()) + ",y=" + str(self.y()) + ",size=" + str(self.size) + "]"
        return "Square [x=" + str(self.x()) + ",y=" + str(self.y()) + ",size=" + str(self.size) + ",color=" + self.color + "]"
        
    def x(self):
        return self.center.x

    def y(self):
        return self.center.y

#Circle
#Defined by providing Point representing center of the shape and it's radius
#Color is optional
class Circle:
    def __init__(self, center, radius, color=None):
        self.center = center
        center.x = float(center.x)
        center.y = float(center.y)
        self.radius = float(radius)
        self.color = color

    def __str__(self):
        if self.color == None:
            return "Circle [x=" + str(self.x()) + ",y=" + str(self.y()) + ",radius=" + str(self.radius) + "]"
        return "Circle [x=" + str(self.x()) + ",y=" + str(self.y()) + ",radius=" + str(self.radius) + ",color=" + self.color + "]"
        
    def x(self):
        return self.center.x

    def y(self):
        return self.center.y