import re

binary_operators = "|&^>="
unary_operators = "!"

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
    state = "get_var_or_unary_op" #initial state
    br = 0 #brackets counter
    e_simplified = re.sub(r'\w+', 'v', e) #simplify the expression - we only need to know if there is a variable - handles 0's and 1' as well
    for char in e_simplified:
        if char == " ": #spaces are omitted
            continue
        if state == "get_var_or_unary_op":
            if char == "v": #variable placeholder found
                state = "get_binary_op" #expect binary operator now
            elif char in unary_operators: #check if the operator is valid
                state = "get_var_or_unary_op" #still expect var or unary operator
            elif char == "(": #opening bracket found
                br += 1
            else:
                return False #expression is invalid
        elif state == "get_binary_op": #else would be good as well but now readability is improved
            if char in binary_operators: #check if the operator is valid
                state = "get_var_or_unary_op" #expect variable or unary operator now
            elif char == ")": #closing bracket found
                br -= 1
            else:
                return False #expression is invalid
        if br < 0:
            return False
    if br == 0 and state == "get_binary_op": #all brackets must be closes and binary operator must be expected
        return True
    else:
        return False

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
def evaluate(e, var_list, binary_input):
    e_eval = e
    for i in range (0, len(binary_input)): #len(binary_input) == len(var_list)
        e_eval = e_eval.replace(var_list[i], binary_input[i]) #replace variable names with values
    operand_stack = []
    operator_stack = []
    for token in e_eval:
        if(token == "1" or token == "0"): #if token is an operand
            operand_stack.append(token)
        elif(token in unary_operators): #if token is a unary operator
            operator_stack.append(token) #push it on the operator stack
        elif(token in binary_operators): #if token is a binary operator
            while operator_stack and operator_stack[-1] in unary_operators: #while there are operators of higher precedence
                #apply them
                operand = operand_stack.pop()
                operator = operator_stack.pop()
                ev = evaluate_unary_operator(operator, operand)
                operand_stack.append(ev)
            operator_stack.append(token)
        elif(token == "("):
            operator_stack.append("(")
        elif(token == ")"):
            while operator_stack and operator_stack[-1] != "(": #until we get back to left paren
                #pop and apply and operator
                operator = operator_stack.pop()
                if(operator in unary_operators):
                    operand = operand_stack.pop()
                    ev = evaluate_unary_operator(operator, operand)
                    operand_stack.append(ev)
                elif(operator in binary_operators):
                    right = operand_stack.pop()
                    left = operand_stack.pop()
                    ev = evaluate_binary_operator(left, operator, right)
                    operand_stack.append(ev)
            operator_stack.pop() #erase the left paren    
    #when processing the expression is finished, apply the rest of operators
    while operator_stack: #while operator stack is not empty
        operator = operator_stack.pop()
        if(operator in unary_operators):
            operand = operand_stack.pop()
            ev = evaluate_unary_operator(operator, operand)
            operand_stack.append(ev)
        elif(operator in binary_operators):
            right = operand_stack.pop()
            left = operand_stack.pop()
            ev = evaluate_binary_operator(left, operator, right)
            operand_stack.append(ev)
    #then, the remainder on the operand stack is the result
    result = operand_stack.pop()
    return result

#Evaluate full expression
#Expression is considered full if it has left and right side
def evaluate_full(e, var_list, binary_input):
    #get both sides of expression and transform them to RPN
    left_side = get_expression_left_side(e)
    right_side = get_expression_right_side(e)
    #get operator to know how to evaluate the full expression
    operator = e[get_separator_index(e)]
    return evaluate_binary_operator(evaluate(left_side, var_list, binary_input), operator, evaluate(right_side, var_list, binary_input))

#Return set of values which (in a form of binary input where n-th bit represents 
#value of n-th variable in given variable list) evaluate the expression to True
def get_expression_true_set(e):
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