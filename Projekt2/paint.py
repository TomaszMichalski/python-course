import sys
import json
from figures import Point
from figures import Polygon
from figures import Rectangle
from figures import Square
from figures import Circle
from painter import Painter
from figures import figure_types
from validator import Validator
from messages import ErrorMessage

def read_json(json_filename):
    with open(json_filename) as json_file:
        data = json.load(json_file)
    return data

def main():
    #Arguement processing
    json_filename = ""
    output_filename = ""
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-o" or sys.argv[i] == "--output": #output filename option
            if Validator.validate_output_flag_use(i + 1, len(sys.argv)):
                i = i + 1
                if output_filename == "":
                    output_filename = sys.argv[i]
            else:
                return
        elif json_filename == "":
            json_filename = sys.argv[i]
        i = i + 1
    if not Validator.validate_input_filename(json_filename):
        return

    #Get json file data
    data = read_json(json_filename)

    #Retrieve palette data
    palette = {}
    if 'Palette' in data:
        palette = data['Palette']
    #Note that palette data is optional
    if not Validator.validate_palette_data(palette):
        return
        
    #Retrieve screen data
    screen = {}
    if Validator.validate_screen_data_existence(data):
        screen = data['Screen']
    else:
        return
    
    if not Validator.validate_screen_data(screen, palette):
        return

    #If bg_color or fg_color are not provided, set them to default (white and black, respectively)
    if 'bg_color' not in screen:
        screen['bg_color'] = "#000000"
    if 'fg_color' not in screen:
        screen['fg_color'] = "#ffffff"

    #Retrieve figures data
    figures = []
    if 'Figures' in data:
        figures = data['Figures']
    #Note that figures data is optional
    if not Validator.validate_figures_data(figures, palette):
        return

    fig_obj = []
    for f in figures:
        t = f['type']
        if t == 'point':
            new_fig = Point(f['x'], f['y'])
        elif t == 'polygon':
            new_fig = Polygon(f['points'])
        elif t == 'rectangle':
            new_fig = Rectangle(Point(f['x'], f['y']), f['width'], f['height'])
        elif t == 'square':
            new_fig = Square(Point(f['x'], f['y']), f['size'])
        elif t == 'circle':
            new_fig = Circle(Point(f['x'], f['y']), f['radius'])
        if 'color' in f:
            new_fig.color = f['color']
        fig_obj.append(new_fig)

    painter = Painter(fig_obj, screen, palette)
    painter.paint()
    if output_filename == "":
        painter.show()
    else:
        painter.show()
        painter.save(output_filename)

if __name__ == "__main__":
    main()