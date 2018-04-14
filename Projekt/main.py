import re

operators = "|&^!>="

#Get distinct list of variable names in expression
def parse_var_names(e):
    result = re.findall(r'[a-zA-z_]\w*', e) #variable may contain alphanumeric characters, but must start with a letter or underscore
    return list(set(result))

#Get expression sides seprator index
#It is the index of "=" or ">"
def get_separator_index(e):
    separator = e.find("=")
    if(separator == -1):
        separator = e.find(">")
    return separator

#Get left side of expression (before ">" or "=")
#If side does not exist, empty string is returned
def get_expression_left_side(e):
    separator = get_separator_index(e)
    if(separator == -1):
        return ""
    return e[:separator]

#Get right of expression (after ">" or "=")
#If side does not exist, empty string is returned
def get_expression_right_side(e):
    separator = get_separator_index(e)
    if(separator == -1):
        return ""
    return e[separator+1:]

#Validate the expression
def validate(e):
    #first level of validation
    number_eq = e.count("=")
    number_impl = e.count(">")
    if((number_eq == 1 and number_impl == 0) or (number_eq == 0 and number_impl == 1)): #one occurence of "=" or ">" should be present, but not both
        if(validate_side(get_expression_left_side(e)) and validate_side(get_expression_right_side(e))): #second level of validation
            return True
        else:
            return False
    else:
        return False

#Validate left or right side of ">" / "=" expresssion
#Or just expression without these operators
def validate_side(e):
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
    e_single = e_single.replace(" ", "") #delete spaces
    m = re.search(r'[a-zA-z_]\w*', e_single) #find the first variable in expression
    if(m.group(0) == e_single): #then it is a single variable - just return it, it is the result
        return e_single
    e_cpy = "(" + e + ")" #add outer parentheses - algorithm needs them
    e_cpy = e_cpy.replace(" ", "") #for convenience
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

#Evaluate given simple logic expression with unary operator
#'!' operator is supported
def evaluate_unary_operator(operator, operand):
    if(operator == "!"):
        if(operand == "1"):
            return "0"
        else:
            return "1"

#Evaluate given simple logic expression with binary operator
#'&', '|', '^', '=', '>' operators are supported
def evaluate_binary_operator(left_operand, operator, right_operand):
    if(operator == "&"):
        if(left_operand == "1" and right_operand == "1"):
            return "1"
        else:
            return "0"
    elif(operator == "|"):
        if(left_operand == "0" and right_operand == "0"):
            return "0"
        else:
            return "1"
    elif(operator == "^"):
        if((left_operand == "1" and right_operand == "0") or (left_operand == "0" and right_operand == "1")):
            return "1"
        else:
            return "0"
    elif(operator == "="):
        if((left_operand == "0" and right_operand == "0") or (left_operand == "1" and right_operand == "1")):
            return "1"
        else:
            return "0"
    elif(operator == ">"):
        if(left_operand == "1" and right_operand == "0"):
            return "0"
        else:
            return "1"

#Evaluate RPN expression using given var list and given binary input
def evaluate(e_rpn, var_list, binary_input):
    print("Evaluating: " + e_rpn)
    print("Variables: " + str(var_list))
    print("Binary input: " + binary_input)
    e_eval = e_rpn
    for i in range (0, len(binary_input)): #len(binary_input) == len(var_list)
        e_eval = e_eval.replace(var_list[i], binary_input[i]) #replace variable names with values
    print("After injecting values: " + e_eval)
    stack = []
    for token in e_eval:
        if(token == " "): #omit spaces
            continue
        elif(token in operators):
            op2 = stack.pop()
            op1 = stack.pop()
            eval = evaluate_binary_operator(op1, token, op2)
            stack.append(eval)
        else: #token is an operand
            stack.append(token)
    result = stack.pop()
    print("Evaluated to: " + result)
    return result

#Evaluate full expression
#Expression is considered full if it has left and right side
def evaluate_full(e, var_list, binary_input):
    #get both sides of expression and transform them to RPN
    left_side = get_expression_left_side(e)
    left_side = rpn(left_side)
    right_side = get_expression_right_side(e)
    right_side = rpn(right_side)
    #get operator to know how to evaluate the full expression
    operator = e[get_separator_index(e)]
    return evaluate_binary_operator(evaluate(left_side, var_list, binary_input), operator, evaluate(right_side, var_list, binary_input))

#Return set of values which (in a form of binary input where n-th bit represents 
#value of n-th variable in given variable list) evaluate the expression to True
def get_expression_true_set(e):
    e_rpn = rpn(e) #get RPN form of the expression
    var_list = parse_var_names(e) #get all variable names in expression
    bits = len(var_list) #binary input should have length equal to number of variables in expression
    result = set()
    for i in range (0, 2 ** bits): #for every possible input bit values
        binary_input = dec_to_bin(i, bits)
        if(evaluate_full(e, var_list, binary_input) == "1"):
            result.add(binary_input)
    return result

#TODO minimalizacja
def minimalize(e, true_set):
    return

def main():
    expression = input("Expression: ")
    if(validate(expression)):
        print("Expression is valid")
        print(get_expression_true_set(expression))
    else:
        print("Expression is invalid")

if __name__ == "__main__":
    main()