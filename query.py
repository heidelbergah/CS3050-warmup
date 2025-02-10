import os
from google.cloud import firestore
from admin import establish_connection
from pyparsing import *

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


def get_input():
    """
    
    """
    valid_input = False
    
    #defines the categories that can be used in a query always at the start of 
    #an expression
    categories = oneOf("manufacturer type rating shelf potassium",as_keyword=True)

    #define acceptable category options for no int category options
    #not adding them as pyparsing rules as I need them in an iterable form
    manufacturer_options = ["American Home Food Products","General Mills",
                            "Kelloggs","Nabisco","Post","Quaker Oats",
                            "Ralston Purina"]
    type_options = ["hot","cold"]

    #define acceptable operators
    operators = (Literal("==") | Literal("<") | Literal(">") | Literal("<=") | 
                 Literal(">=") | Literal("!="))
    lpar = Literal("(")
    rpar = Literal(")")
    logical_operators = oneOf("and or")
    
    #parse action for expressions
    def expression_parse(tokens):
        categories, _, value = tokens
        value = " ".join(value) if isinstance(value, list) else value
        match categories:
            case "manufacturer":
                if value not in manufacturer_options:
                    raise ValueError("Invalid manufacturer")
            case "type":    
                if value not in type_options:
                    raise ValueError("Invalid type")
            case "rating": 
                if int(value) not in range(101):
                    raise ValueError("Invalid rating")
            case "shelf":
                if int(value) not in range(1,4):
                    raise ValueError("Invalid shelf")
            case "potassium": 
                if int(value) not in range(1001):
                    raise ValueError("Invalid potassium")
        return tokens
    
    #value can take a string or integer and will stop when it reaches a logical operator
    #the list of strings if it was more than one is then joined together
    value = OneOrMore(Word(alphanums)).stopOn(logical_operators).setParseAction(lambda t: " ".join(t))

    #expression does not handle logical operators
    #example: manufacturer == Kelloggs
    expression = categories + operators + value
    expression.setParseAction(expression_parse)

    #basic query is a series of expressions with logical operators between them
    basic_query = OneOrMore(expression + logical_operators) + expression

    #closed query is a basic query enclosed in parentheses
    closed_query = lpar + basic_query + rpar

    #adds together expressions with logical operators and additional expressions 
    query_language = (ZeroOrMore(closed_query) + logical_operators + basic_query + logical_operators + ZeroOrMore(closed_query) |
                      ZeroOrMore(basic_query) + logical_operators + closed_query + logical_operators + ZeroOrMore(basic_query) |
                      OneOrMore(basic_query + logical_operators + closed_query))
    
    while not valid_input:
        #initial prompt for input 
        user_input = input("Please enter your query if you need help type \'help\'\n>>")
        print("\n")#for output readability
        
        #pyparsing uses spaces as a delimiter so I need to add spaces around parentheses
        if "(" in user_input:
            user_input = user_input.replace('(','( ')
        if ")" in user_input:
            user_input = user_input.replace(')',' )')
        print(user_input)
            
        if user_input.lower() ==  "exit":
            return user_input

    
        elif user_input == "help":
            print("Query Language:\nmanufacuter: manufacturer of the cereal\n" + 
                  "type: type of cereal, cold or hot\n" + 
                  "rating: rating of cereal 0-100\n" + 
                  "shelf: shelf from the floor 1,2,3\n" + 
                  "potassium: amount of potassium in cereal\n" + 
                  "and: and\nor: or\n<: less than\n<=: less than or equal to\n" + 
                  ">: greater than\n>=: greater than or equal to\n" + 
                  "==: is or equal to\n(): allows for compound expressions\n" + 
                  "!: negative operator\n\nExamples:\n" + 
                  "manufacuter == Kelloggs and potassium > 0\n" + 
                  "shelf == 3 or potassium > 0\n" + 
                  "Queries are case sensitive\n")
        else:
            valid_input = True
            try:
                query_language.parseString(user_input)
            except Exception as e:
                print(f"Error: {e}")
                valid_input = False
                print("\n")#for output readability
        
    return user_input

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
        return_list.append(f"{doc.to_dict()['name']}")

    return return_list


def execute_query(query):
    fancy_print(retrieve_query(parse_query(query)))


def fancy_print(cereals):
    if len(cereals) == 0:
        print("No cereals meet these requirements!")
    for cereal in cereals:
        print(f"- {cereal}")


#execute_query("shelf == 1 and manufacturer == Nabisco")
#get_input()

"""
# Define a main program to loop through the
Prompts for a query.
Runs the query and displays results.
Allows the user to keep making additional queries or type exit to end program.
"""
def main():
    """
    Allows program to run on a loop and provides option to exit the program 
    """
    print("Welcome to the Cereal Query Program!")
    print("Type 'help' to see query instructions or 'exit' to quit.\n")
    run_program = True
    while run_program == True:
        # Get the query from the user
        user_query = get_input()
        # Check if user wants to exit 
        if user_query.lower() == "exit":
            print("Exiting the Cereal Query Program. Goodbye!")
            break
            
        
        try:
            # Execute the query and print the results
            execute_query(user_query)
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the program            
if __name__ == "__main__":
    main()