class ErrorMessage:
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

    def invalid_output_flag_use():
        print("Invalid use of -o/--output flag")

    def no_input_filename():
        print("No input filename provided")

    def no_screen_data():
        print("No 'Screen' data provided. JSON file is invalid")

    def unknown_type_for_figure(figure_type, figure):
        print("Unknown type '" + figure_type + "' for figure: " + str(figure))
    
