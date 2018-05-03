from figures import Point
from figures import Polygon
from figures import Rectangle
from figures import Square
from figures import Circle
from figures import figure_types
import png

class Painter:
        def __init__(self, figures, screen, palette):
            self.figures = figures
            self.screen = screen
            self.palette = palette

        def paint(self):
            canvas = []
            bg_color = self.convert_color(self.screen['bg_color'])
            for i in range (0, self.screen['height']):
                canvas.append([])
                for j in range (0, self.screen['width']):
                    canvas[i] += bg_color
            for figure in self.figures:
                if isinstance(figure, Point):
                    canvas = self.paint_point(canvas, figure)

            for i in range (0, len(canvas)):
                canvas[i] = tuple(canvas[i])

            with open("out.png", 'wb') as output_file:
                w = png.Writer(self.screen['width'], self.screen['height'])
                w.write(output_file, canvas)
            png.from_array(canvas, 'RGB').save('test.png')

        def paint_point(self, canvas, point):
            color = self.get_color(point)
            if self.possible_to_draw(canvas, point):
                canvas[point.y][3 * point.x] = color[0]
                canvas[point.y][3 * point.x + 1] = color[1]
                canvas[point.y][3 * point.x + 2] = color[2]
            return canvas

        def possible_to_draw(self, canvas, point):
            if len(canvas) == 0 or len(canvas[0]) == 0:
                return False
            if point.y >= 0 and point.y < len(canvas) and point.x >= 0 and 3 * point.x < len(canvas[0]): #possible to draw
                return True
            return False

        def get_color(self, figure):
            if figure.color == None:
                return self.convert_color(self.screen['fg_color'])
            else:
                return figure.color

        def convert_color(self, color):
            if color in self.palette: #if color is in palette, retrieve it's actual form
                color = self.palette[color]
            res = []
            if color[0] == "#": # #rrggbb form
                res += [int(color[1:3], 16)]
                res += [int(color[3:5], 16)]
                res += [int(color[5:], 16)]
            else: # (r,g,b) form
                color = color[1:-1]
                for num in color.split(","):
                    res += [num]
            return res
            