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
    if(number_eq > 1 or number_impl > 1): #simple syntax check
        return False
    elif((number_eq == 1 and number_impl == 0) or (number_eq == 0 and number_impl == 1)): #one occurence of "=" or ">" should be present, but not both
        if(validate_side(get_expression_left_side(e)) and validate_side(get_expression_right_side(e))): #second level of validation
            return True
        else:
            return False
    elif(get_separator_index(e) == -1 and validate_side(e)): #this means that expression has no "=" or ">" operator
        return True
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
    if(bits < 1):
        return ""
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
    if(get_separator_index(e) == -1): #no "=" or ">" operator
        return evaluate(e, var_list, binary_input)
    else:
        #get both sides of expression and transform them to RPN
        left_side = get_expression_left_side(e)
        right_side = get_expression_right_side(e)
        #get operator to know how to evaluate the full expression
        operator = e[get_separator_index(e)]
        return evaluate_binary_operator(evaluate(left_side, var_list, binary_input), operator, evaluate(right_side, var_list, binary_input))

#Return set of values which (in a form of binary input where n-th bit represents 
#value of n-th variable in given variable list) evaluate the expression to True
def get_expression_true_list(e):
    var_list = parse_var_names(e) #get all variable names in expression
    bits = len(var_list) #binary input should have length equal to number of variables in expression
    result = []
    for i in range (0, 2 ** bits): #for every possible input bit values
        binary_input = dec_to_bin(i, bits)
        if(evaluate_full(e, var_list, binary_input) == "1"):
            result.append(binary_input)
    return result

#Counts "1" occurences in given input string
def count_ones(input):
    result = 0
    for bit in input:
        if(bit == "1"):
            result += 1
    return result

#Combines two binary inputs into one if it is possible - if the vary by a single bit
#If combination is impossible, empty string is returned
def combine(first, second):
    count = 0 #count of digits that vary
    length = len(first) #equal to len(second)
    result = ""
    if first and second:
        for i in range(0, length):
            if(first[i] != second[i]):
                result += "-"
                count += 1
            else:
                result += first[i] #+= second[i]
        if(count > 1):
            return ""
        else:
            return result
    else:
        return ""

#Processes Quine-McCluskey groups until no more combinations can be performed
def process_groups(groups):
    changed = False #flag that indicates if any change has been made this time
    groups_quantity = len(groups)
    for i in range(0, groups_quantity - 1): #for every groups except the last one
        for first in groups[i]: #process every item in this group
            for second in groups[i + 1]: #with every item in the next group
                combination = combine(first, second)
                if combination: #if the combination result exists
                    #remove both
                    groups[i].remove(first)
                    groups[i + 1].remove(second)
                    #and add the result
                    groups[i].append(combination)
                    changed = True
                    break
    if changed:
        process_groups(groups)

#Maps the given binary grouping result with variable list, creating minimalisation result element
def get_result_element(var_list, bits):
    result = ""
    for i in range(0, len(var_list)):
        if(bits[i] == "1"):
            result += " " + var_list[i]
        elif(bits[i] == "0"):
            result += " " + var_list[i] + "'"
    return result[1:] #just to omit the space at the beggining

#Generate possible values out of grouped binary input
def generate_binary_input(grouped_input):
    gen = [grouped_input]
    while gen and len(gen) != len(grouped_input):
        current = gen[0]
        for i in range(0, len(current)):
            if(current[i] == "-"):
                gen.append(current[:i] + "0" + current[i+1:])
                gen.append(current[:i] + "1" + current[i+1:])
                gen.remove(current)
                break
    return gen

#TODO dodać tą tabelkę z wykreślaniem
def minimalize(e, var_list, true_list):
    if(len(true_list) == 0): #always evaluates to 0
        return "0"
    if(len(true_list) == 2 ** len(var_list)): #always evaluates to 1
        return "1"
    groups_quantity = len(true_list[0]) + 1 #number of bits in any element of that set + 1 is the number of groups in Quinn-McCluskey algorithm
    groups = []
    for i in range(0, groups_quantity): #instantiate empty groups
        groups.append([])
    for input in true_list: #fill the groups
        groups[count_ones(input)].append(input)
    process_groups(groups)
    result = ""
    for group in groups:
        for item in group:
            if result:
                result += " + " + get_result_element(var_list, item)
            else:
                result = get_result_element(var_list, item)
    return result
            
#Run the Quine-McCluskey algorithm for given expression
def quine_mccluskey(e):
    if(validate(e)):
        print("Result: " + minimalize(e, parse_var_names(e), get_expression_true_list(e)))
    else:
        print("Expression is invalid")

def main():
    expression = input("Expression: ")
    quine_mccluskey(expression)

if __name__ == "__main__":
    main()