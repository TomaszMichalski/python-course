from figures import Point
from figures import Polygon
from figures import Rectangle
from figures import Square
from figures import Circle
from figures import figure_types
from PIL import Image, ImageDraw

class Painter:
        def __init__(self, figures, screen, palette):
            self.figures = figures
            self.screen = screen
            self.palette = palette

        def paint(self):
            size = (self.screen['width'], self.screen['height'],)
            self.canvas = Image.new('RGB', size, self.convert_color(self.screen['bg_color']))
            for figure in self.figures:
                if isinstance(figure, Point):
                    self.paint_point(figure)
                elif isinstance(figure, Polygon):
                    self.paint_polygon(figure)
                elif isinstance(figure, Rectangle):
                    self.paint_rectangle(figure)
                elif isinstance(figure, Square):
                    self.paint_square(figure)
                elif isinstance(figure, Circle):
                    self.paint_circle(figure)

        def show(self):
            self.canvas.show()

        def save(self, filepath):
            if not filepath.endswith(".png"):
                filepath = filepath + ".png"
            self.canvas.save(filepath)

        def paint_point(self, point):
            draw = ImageDraw.Draw(self.canvas)
            draw.point([point.x, point.y], self.get_color(point))

        def paint_polygon(self, polygon):
            draw = ImageDraw.Draw(self.canvas)
            points = []
            for point in polygon.points:
                points.append(point.x)
                points.append(point.y)
            draw.polygon(points, self.get_color(polygon))

        def paint_rectangle(self, rectangle):
            draw = ImageDraw.Draw(self.canvas)
            box = [rectangle.x() - rectangle.width / 2, rectangle.y() - rectangle.height / 2, rectangle.x() + rectangle.width / 2, rectangle.y() + rectangle.height / 2]
            draw.rectangle(box, self.get_color(rectangle))

        def paint_square(self, square):
            draw = ImageDraw.Draw(self.canvas)
            box = [square.x() - square.size / 2, square.y() - square.size / 2, square.x() + square.size / 2, square.y() + square.size / 2]
            draw.rectangle(box, self.get_color(square))

        def paint_circle(self, circle):
            draw = ImageDraw.Draw(self.canvas)
            box = [circle.x() - circle.radius, circle.y() - circle.radius, circle.x() + circle.radius, circle.y() + circle.radius]
            draw.ellipse(box, self.get_color(circle))

        def get_color(self, figure):
            if figure.color == None:
                return self.convert_color(self.screen['fg_color'])
            else:
                return self.convert_color(figure.color)

        def convert_color(self, color):
            if color in self.palette: #if color is in palette, retrieve it's actual form
                color = self.palette[color]
            res = ()
            if color[0] == "#": # #rrggbb form
                res += (int(color[1:3], 16),)
                res += (int(color[3:5], 16),)
                res += (int(color[5:], 16),)
            else: # (r,g,b) form
                color = color[1:-1]
                for num in color.split(","):
                    res += (int(num),)
            return res