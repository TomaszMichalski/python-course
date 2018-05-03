import sys
import json
import string
from figures import Point
from figures import Polygon
from figures import Rectangle
from figures import Square
from figures import Circle

figure_types = ["point", "polygon", "rectangle", "square", "circle"]

def read_json(json_filename):
    with open(json_filename) as json_file:
        data = json.load(json_file)
    return data

def validate_screen_data(screen, palette):
    if 'width' not in screen:
        no_property("width", screen)
        return False
    if 'height' not in screen:
        no_property("height", screen)
        return False
    if 'bg_color' in screen and not validate_colour(screen['bg_color']) and not is_key_in_palette(screen['bg_color'], palette):
        invalid_property_value("bg_color", screen['bg_color'], screen)
        return False
    if 'fg_color' in screen and not validate_colour(screen['fg_color']) and not is_key_in_palette(screen['fg_color'], palette):
        invalid_property_value("fg_color", screen['fg_color'], screen)
        return False
    return True

def validate_palette_data(palette):
    for key in palette:
        colour = palette[key]
        if not validate_colour(colour):
            invalid_value_for_key(key, colour, screen)
            return False

    return True

def validate_colour(colour):
    if colour == "":
        return False
    else:
        if(colour[0] == "#"): # #rrggbb form
            return all(c in string.hexdigits for c in colour[1:])
        elif colour[0] == "(" and colour[-1] == ")":
            colour = colour[1:-1]
            rgb_values = colour.split(",")
            if len(rgb_values) != 3:
                return False
            for i in range (0, 3):
                try:
                    rgb_values[i] = int(rgb_values[i])
                except:
                    return False
                    
            return all(val < 256 and val >= 0 for val in rgb_values)
        else:
            return False

def is_key_in_palette(key, palette):
    return key in palette

def validate_figures_data(figures, palette):
    for figure in figures:
        #Check if 'type' property exists
        if 'type' not in figure:
            no_property("type", figure)
            return False
        t = figure['type']
        #Check if 'type' property is valid
        if t not in figure_types:
            unknown_type_for_figure(t, figure)
            return False
        #Check if coords are valid (if necessary)
        if t != "polygon" and not validate_coord(figure):
            return False
        #Check special figure properties (based on it's type)
        if not validate_special_properties(figure):
            return False
        #Check color, if it exists
        if 'color' in figure and not validate_colour(figure['color']) and not is_key_in_palette(figure['color'], palette):
            invalid_property_value("color", figure['color'], figure)
            return False

    return True

def validate_coord(figure):
    if 'x' not in figure:
        no_property("x", figure)
        return False
    if 'y' not in figure:
        no_property("y", figure)
        return False
    if not isnumber(figure['x']):
        property_not_a_number("x", figure)
        return False
    if not isnumber(figure['y']):
        property_not_a_number("y", figure)
        return False
    return True

def validate_special_properties(figure):
    t = figure['type']
    if t == "polygon":
        if 'points' in figure: #note that 'points' property is not required
            points = figure['points']
            if not isinstance(points, list):
                property_is_not_list("points", figure)
                return False
            for i in range (0, len(points)):
                if not isinstance(points[i], list):
                    property_is_not_list("points[" + i + "]", figure)
                    return False
                if len(points[i]) != 2 or not isnumber(points[i][0]) or not isnumber(points[i][1]):
                    invalid_coordinates("points[" + i + "]", points[i])
                    return False
    elif t == "rectangle":
        if 'width' not in figure:
            no_property("width", figure)
            return False
        if 'height' not in figure:
            no_property("height", figure)
            return False
        if not isnumber(figure['width']):
            property_not_a_number("width", figure)
            return False
        if not isnumber(figure['height']):
            property_not_a_number("height", figure)
            return False
    elif t == "square":
        if 'size' not in figure:
            no_property("size", figure)
            return False
        if not isnumber(figure['size']):
            property_not_a_number("size", figure)
            return False
    elif t == "circle":
        if 'radius' not in figure:
            no_property("radius", figure)
            return False
        if not isnumber(figure['radius']):
            property_not_a_number("radius", figure)
            return False
    
    return True

def no_property(prop, obj):
    print("No '" + prop + "' property for object " + str(obj))

def property_not_a_number(prop, obj):
    print("'" + prop + "' property is not a number for object " + str(obj))

def unknown_type(type_value, obj):
    print("Unknown 'type' value: " + type_value + " for object " + str(obj))

def invalid_value_for_key(key, value, obj):
    print("Value " + value + " invalid. Key = " + key + ". Object = " + str(obj))

def invalid_property_value(name, value, obj):
    print("'" + name + "' property is invalid: " + value + ". Object = " + str(obj))

def property_is_not_list(name, obj):
    print("'" + name + "' property is not a list for object " + str(obj))

def invalid_coordinates(name, value):
    print("Invalid coordinates: " + name + " = " + str(value))

def isnumber(num):
    try:
        float(num)
    except:
        return False
    return True

def main():
    #Arguement processing
    json_filename = ""
    output_filename = ""
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-o" or sys.argv[i] == "--output": #output filename option
            if(i + 1 < len(sys.argv)): #output filename is provided
                i = i + 1
                if output_filename == "":
                    output_filename = sys.argv[i]
            else:
                print("Invalid use of -o/--output flag")
                return
        elif json_filename == "":
            json_filename = sys.argv[i]
        i = i + 1
    if(json_filename == ""): #no input filename provided
        print("No input filename provided")
        return

    #Get json file data
    data = read_json(json_filename)

    #Retrieve palette data
    palette = {}
    if 'Palette' in data:
        palette = data['Palette']
    #Note that palette data is optional
    if not validate_palette_data(palette):
        print("Palette data is invalid")
        return
        
    #Retrieve screen data
    screen = {}
    if 'Screen' in data: #first level of validation - there must be any screen data
        screen  = data['Screen']
    else:
        print("No 'Screen' data provided. JSON file is invalid")
        return
    
    if not validate_screen_data(screen, palette):
        print("Screen data is invalid")
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
    if not validate_figures_data(figures, palette):
        print("Figures data is invalid")
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

    for figure in fig_obj:
        print(figure)

    
    print("So far so good")

if __name__ == "__main__":
    main()