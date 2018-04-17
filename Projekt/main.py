import re

binary_operators = "|&^>="
unary_operators = "!"

#Get distinct list of variable names in expression
def parse_var_names(e):
    result = re.findall(r'[a-zA-Z_]\w*', e) #variable may contain alphanumeric characters, but must start with a letter or underscore
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
            while operator_stack: #while there are operators of higher precedence, apply them
                if operator_stack[-1] in unary_operators:
                    operand = operand_stack.pop()
                    operator = operator_stack.pop()
                    ev = evaluate_unary_operator(operator, operand)
                    operand_stack.append(ev)
                elif operator_stack[-1] == "&":
                    right = operand_stack.pop()
                    left = operand_stack.pop()
                    operator = operator_stack.pop()
                    ev = evaluate_binary_operator(left, operator, right)
                    operand_stack.append(ev)
                else:
                    break
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

#Return set of values which (in a form of binary input where n-th bit represents 
#value of n-th variable in given variable list) evaluate the expression to True
def get_expression_true_list(e):
    var_list = parse_var_names(e) #get all variable names in expression
    bits = len(var_list) #binary input should have length equal to number of variables in expression
    result = []
    for i in range (0, 2 ** bits): #for every possible input bit values
        binary_input = dec_to_bin(i, bits)
        if(evaluate(e, var_list, binary_input) == "1"):
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
    new_groups = [] #list of lists of processsed input
    used_input = [] #this will mark if input in pre-processed groups was used
    groups_quantity = len(groups)
    for i in range(0, groups_quantity):
        new_groups.append([])
        used_input.append([])
        for j in range(0, len(groups[i])):
            used_input[i].append(False)
    #now let's process the groups!
    changed = False #flag that will indicate when to stop processing
    for i in range(0, groups_quantity - 1): #for every group except the last one
        for item_index in range(0, len(groups[i])): #for every item in i-th group
            for item2_index in range(0, len(groups[i+1])): #for every item in i+1-th group
                comb = combine(groups[i][item_index], groups[i + 1][item2_index]) #try to combine them
                if comb: #if comb is not an empty string, so the merging was successful
                    new_groups[count_ones(comb)].append(comb) #append it to proper new group
                    used_input[i][item_index] = True #mark as used
                    used_input[i + 1][item2_index] = True #mark as used
                    changed = True #note that change has been made
    #another round of processing has finished
    for i in range(0, groups_quantity): #check if there are unused inputs - they need to be saved
        for item_index in range(0, len(groups[i])):
            if(used_input[i][item_index] == False): #if the input is unused
                new_groups[count_ones(groups[i][item_index])].append(groups[i][item_index]) #append it as it was to the new group
    groups = new_groups #we can forget about the used ones
    #now it's time to erase duplicates in each group
    for i in range(0, groups_quantity): #process every group
        groups[i] = list(set(groups[i])) #make set out of the list, then make it a list 
    if changed:
        groups = process_groups(groups) #if there was a change, call processing again
    return groups

#Maps the given binary grouping result with variable list, creating minimalisation result element
def get_result_element(var_list, bits):
    result = ""
    for i in range(0, len(var_list)):
        if(bits[i] == "1"):
            result += " " + var_list[i]
        elif(bits[i] == "0"):
            result += " " + var_list[i] + "'"
    return result[1:] #just to omit the space at the beggining

#Returns number of "-" in grouped input
def get_placeholders_num(grouped_input):
    res = 0
    for token in grouped_input:
        if(token == "-"):
            res += 1
    return res

#Generate possible values out of grouped binary input
def generate_binary_input(grouped_input):
    gen = [grouped_input]
    while gen and len(gen) != 2 ** get_placeholders_num(grouped_input):
        current = gen[0]
        for i in range(0, len(current)):
            if(current[i] == "-"):
                gen.append(current[:i] + "0" + current[i+1:])
                gen.append(current[:i] + "1" + current[i+1:])
                gen.remove(current)
                break
    return gen

#Initialize chart of width = length of list of input that cause the expression to evaluate to true
#heigth = number of items after first stage minimalisation (process_groups)
def initialize_chart(true_list, items):
    chart = []
    for x in range (len(items)):
        chart.append([])
        for y in range (len(true_list)):
            chart[x].append(0)
    #now the chart is filled with 0's
    #fill 1's in correct places
    for item_index in range (len(items)): #process each item
        for input in generate_binary_input(items[item_index]): #for every input it generates (like '-1' generates '01' and '11')
            for true_list_index in range (len(true_list)): #process each true-evaluating input
                if(input == true_list[true_list_index]): #if item generates the true-evaluating input
                    chart[item_index][true_list_index] = 1
    return chart

#Return the essential primes using given chart, variable names list and items (like '1-00) list
def get_essential_primes(chart, var_list, items):
    primes = []
    for column in range(0, len(chart[0])): #length of every chart row is the same, and equal to number of columns
        count = 0 #numer of 1's in column
        for row in range(0, len(chart)): #number of rows
            if(chart[row][column] == 1):
                count += 1
                essential_row = row #save row of 1 occurence in potential essential prime
        
        if(count == 1): #essential prime found
            primes.append(get_result_element(var_list, items[essential_row]))
            #erase all columns that are covered by found essential prime
            for i in range(0, len(chart[0])):
                if(chart[essential_row][i] == 1): #found a column to erase
                    for j in range(0, len(chart)): #erase the column
                        chart[j][i] = 0
    return list(set(primes))

#Check if there are only 0's in chart
def check_chart_all_zero(chart, rows, columns):
    for i in range(0, rows):
        for j in range(0, columns):
            if(chart[i][j] != 0):
                return False
    return True

#Given the result items, connect them into a single string
def get_result(items):
    result = ""
    for item in items:
        result += " + " + item
    return result[3:] #omit the first " + "

#Multiplicates two factors in Petrick's method
def multiplicate(factor, factor2):
    #simple cases
    if factor == [] and factor2 == []:
        return []
    if factor == []:
        return factor2
    if factor2 == []:
        return factor
    result = []
    for i in factor:
        for j in factor2:
            if(i == j):
                result.append(i) #append only one
            else:
                result.append(list(set(i+j))) #append both
    return result

#Calculates "cost" of prime - which is the number of variables in it
def calculate_prime_cost(prime):
    cost = 0
    for token in prime:
        if(token != "-"):
            cost += 1
    return cost

#TODO Petrick's method
def petricks(chart, items, var_list):
    factors = [] #this will hold all factors, like (R1 + R3) (either row 1 or row 3 must be in result)
    for col in range(0, len(chart[0])):
        factor = []
        for row in range(0, len(chart)):
            if(chart[row][col] == 1):
                factor.append([row])
        if(factor != []):
            factors.append(factor)
    #multiplicate factors
    for i in range(0, len(factors) - 1):
        factors[i + 1] = multiplicate(factors[i], factors[i + 1])
    
    multiplied = factors[-1]
    multiplied = sorted(multiplied, key=len)
    min_length = len(multiplied[0]) #length of the first one is the length of products we are looking for
    primes = []
    for product in multiplied:
        if len(product) == min_length:
            primes.append(product)

    #calculate each prime combination cost
    prime_cost = []
    for prime in primes:
        cost = 0
        for i in range(0, len(items)):
            for item_index in prime:
                cost += calculate_prime_cost(items[item_index])
        prime_cost.append(cost)
    #get minimum cost combinations
    prime_min = []
    for i in range(0, len(prime_cost)):
        if prime_cost[i] == min(prime_cost):
            prime_min.append(primes[i])
    primes_literals = [] #primes represented as literals, i.e A'BC
    for p in prime_min[0]: #each of prime_min[i] has equal cost so it does not matter which we choose
        primes_literals.append(get_result_element(var_list, items[p]))
    return primes_literals

#Minimalize given expression using Quine-McCluskey algorithm and Petrick's method
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
    groups = process_groups(groups)
    result = ""
    #flatten the groups list of lists to a one-dimension list
    items = []
    for group in groups:
        for item in group:
            items.append(item)
    #get the initialized chart
    chart = initialize_chart(true_list, items)
    #get essential primes using the chart
    essential_primes = get_essential_primes(chart, var_list, items)
    if(check_chart_all_zero(chart, len(items), len(true_list))): #if chart is already all 0's, there is no need to do Patrick's algorithm
        return get_result(essential_primes)
    else:
        return get_result(essential_primes) + " + " + get_result(petricks(chart, items, var_list))
            
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