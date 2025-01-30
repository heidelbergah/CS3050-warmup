import os
from google.cloud import firestore
from admin import establish_connection

"""
NOTES

1. The conditional_operators probably aren't even necessary anymore.
   If the only conditional operator allowed is "and", they why even
   bother tracking it if we already know what it'll be?

TODO

1. Add functionality for the "help" keyword
2. Bugtest. Just try to break the program and place any found bugs in
   the BUGS section.

BUGS

"""

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

        #checks if parts[x] is a category and if so takes the next 3 elements of 
        #parts and makes them into a tuple that is added to logic_statments_return
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


def retrieve_query(parsed_input):
    expressions = parsed_input[0]
    operators = parsed_input[1] # May not even be necessary :p

    db = establish_connection() # So happy I put this in a function in admin.py
    cereal_data = db.collection("cereal_data")

    query = cereal_data

    for expression in expressions:
        param_type = ""
        comparator = ""
        value = ""

        # A bunch of match statements to transform strings to their
        # appropriate query values. A dictionary could probably also
        # accomplish this, but this is the easiest. We can modify in
        # future if so desired.
        match expression[0]:
            case "manufacturer":
                param_type = "mfr"
            case "type":
                param_type = "type"
            case "rating":
                param_type = "rating"
            case "shelf":
                param_type = "shelf"
            case "potassium":
                param_type = "potass"
            case _:
                return "Not a valid parameter type"

        match expression[1]:
            case "==":
                comparator = "=="
            case "<":
                comparator = "<"
            case ">":
                comparator = ">"
            case "<=":
                comparator = "<="
            case ">=":
                comparator = ">="
            case "!=":
                comparator = "!="
            case _:
                return "Not a valid comparator"

        match expression[2]:
            case "American":
                value = "A"
            case "General":
                value = "G"
            case "Kellogs":
                value = "K"
            case "Nabisco":
                value = "N"
            case "Post":
                value = "P"
            case "Quaker":
                value = "Q"
            case "Ralston":
                value = "R"
            case "hot":
                value = "H"
            case "cold":
                value = "C"
            case _:
                value = float(expression[2]) # If not a string, probably a num
                                             # Will update in the future.

        # Update the current query with another where clause.
        query = query.where(filter=firestore.FieldFilter(param_type, comparator, value))
        
    # Pull the results from the query we just made
    results = query.stream()

    # Put all of the names into a return list. We can add more data than just
    # the cereal name if we want to.
    return_list = []
    for doc in results:
        return_list.append(f"{doc.to_dict()["name"]}")

    return return_list


def execute_query(query):
    fancy_print(retrieve_query(parse_query(query)))


def fancy_print(cereals):
    if len(cereals) == 0:
        print("No cereals meet these requirements!")
    for cereal in cereals:
        print(f"- {cereal}")


execute_query("shelf == 1 and manufacturer == Nabisco")

