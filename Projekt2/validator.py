import string
from figures import figure_types

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