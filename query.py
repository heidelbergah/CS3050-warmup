import os
#from google.cloud import firestore

def parse_query(input_query):
    parts = input_query.split(' ')

    unclosed_parentheses = False
    operators = ["and","or"]
    categories = ["manufacturer","type","rating","shelf","potassium"]

    #index in the logic_statements_return list that is being edited 
    active_return_list_index = 0
    #the two lists that are returned 
    logical_operators_return = []
    logic_statments_return = []  
    for x in range(len(parts)): 

        if '(' in parts[x]:
            if unclosed_parentheses:
                return "parse error no double nesting parentheses"
            else:
                logic_statments_return.append([])
                unclosed_parentheses = True
                parts[x] = parts[x][1:]

        if ')' in parts[x]:
            if not unclosed_parentheses:
                return "parse error '(' is expected before ')'"
            unclosed_parentheses = False
            parts[x] = parts[x][:-1]


        if parts[x] in categories:
            if unclosed_parentheses:
                if ')' in parts[x + 2]:
                    parts[x + 2] = parts[x + 2][:-1]
                    unclosed_parentheses = False
                logic_statments_return[active_return_list_index].append((parts[x], parts[x + 1], parts[x + 2]))
            else:
                logic_statments_return.append((parts[x], parts[x + 1], parts[x + 2]))
                active_return_list_index += 1

        if parts[x] in operators:
            logical_operators_return.append(parts[x])

    return (logic_statments_return,logical_operators_return)

print(parse_query("manufacturer == General Mills and potassium > 0"))

#def get_input():


    