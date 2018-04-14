import re

operators = "|&^!>="

#Get distinct list of variable names in expression
def parse_var_names(e):
    result = re.findall(r'[a-zA-z_]\w*', e) #variable may contain alphanumeric characters, but must start with a letter or underscore
    return list(set(result))

#Validate the expression
def validate(e):
    state = "get_var" #initial state
    br = 0 #brackets counter
    e_simplified = re.sub(r'\w+', 'v', e) #simplify the expression - we only need to know if there is a variable - handles 0's and 1' as well
    for char in e_simplified:
        if char == " ": #spaces are omitted
            continue
        if state == "get_var":
            if char == "v": #variable placeholder found
                state = "get_op" #expect operator now
            elif char == "(": #opening bracket found
                br += 1
            else:
                return False #expression is invalid
        elif state == "get_op": #else would be good as well but now readability is improved
            if char in operators: #check if the operator is valid
                state = "get_var" #expect variable now
            elif char == ")": #closing bracket found
                br -= 1
            else:
                return False #expression is invalid
        if br < 0:
            return False
    if br == 0 and state == "get_op": #all brackets must be closes and operator must be expected
        return True
    else:
        return False

#Convert the expression to reverse Polish notation
def rpn(e):
    result = ""
    #check if e is a single variable - it is a special case
    e_single = e
    e_single = e_single.replace("(", "") #delete left brackets
    e_single = e_single.replace(")", "") #delete right brackets
    m = re.search(r'[a-zA-z_]\w*', e_single) #find the first variable in expression
    if(m.group(0) == e_single): #then it is a single variable - just return it, it is the result
        return e_single
    e_cpy = "(" + e + ")" #add outer parentheses - algorithm needs them
    e_cpy = e_cpy.replace(" ", "") #for convenience
    print(e_cpy)
    def rpn_inner():
        nonlocal result
        nonlocal e_cpy
        if(e_cpy[0] == "("): #get first char
            c = e_cpy[0]
        else: #or variable name
            c = re.search(r'[a-zA-Z_]\w*', e_cpy).group(0)
        if(c == "("):
            e_cpy = e_cpy[1:]
            rpn_inner()
            a = e_cpy[0] #always operand
            e_cpy = e_cpy[1:] #delete parsed char
            rpn_inner()
            e_cpy = e_cpy[1:] #delete char - always closing bracket
            result = result + " " + a
        else:
            result = result + " " + c
            e_cpy = e_cpy[len(c):] #delete parsed char
    rpn_inner()
    return result

#Convert the given number to binary, result will have given number of bits
def dec_to_bin(number, bits):
    result = bin(number)
    result = result[2:] #cut off the '0b'
    result = ("0" * (bits - len(result))) + result
    return result

#TODO ewaluacja wyrazenia przy podaniu n-bitowej liczby dla n bitów
def evaluate(e_rpn, var_list, bits):

#TODO wyznaczenie wartosci, dla których wyrażenie jest prawdziwe
def get_expression_true_set(e):
    var_list = parse_var_names(e) #get distinct list of variables
    e_rpn = rpn(e)
    result = set()
    for i in range (0, len(var_list)): #for every possible input bit values
        if(evaluate(e_rpn, var_list, dec_to_bin(i))): #if the expression evaluates to True for given input
            result.add(dec_to_bin(i))
    return result

#TODO minimalizacja
def minimalize(e, true_set):
    return

def main():
    print(dec_to_bin(4, 5))
    expression = input("Expression: ")
    #first level of validation
    number_eq = expression.count("=")
    number_impl = expression.count(">")
    if((number_eq == 1 and number_impl == 0) or (number_eq == 0 and number_impl == 1)): #one occurence of "=" or ">" should be present, but not both
        #find index of the separation between left and right side of expression (index of "=" or ">")
        separator = expression.find("=")
        if(separator == -1):
            separator = expression.find(">")
        #split the expression
        left_side = expression[:separator]
        right_side = expression[separator+1:]

        if(validate(left_side) and validate(right_side)): #second level of validation
            var_names_left = parse_var_names(left_side) #get set of variable names of the left side of expression
            print(var_names_left)
            var_names_right = parse_var_names(right_side) #get set of variable names of the right side of expression
            print(var_names_right)
            print(rpn(left_side))
            print(rpn(right_side))
        else:
            print("Expression is invalid")
    else:
        print("Expression is invalid")


if __name__ == "__main__":
    main()