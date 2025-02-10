import os
#from google.cloud import firestore
#from admin import establish_connection
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

    #define acceptable operators
    operators = (Literal("==") | Literal("<") | Literal(">") | Literal("<=") | 
                 Literal(">=") | Literal("!="))
    lpar = Literal("(")
    rpar = Literal(")")
    logical_operators = oneOf("and or")
    
    #parse action for expressions
    def expression_parse(tokens):
        categories, _, value = tokens
        match categories:
            case "manufacturer":
                if value not in ["American Home Food Products","General Mills",
                            "Kelloggs","Nabisco","Post","Quaker Oats",
                            "Ralston Purina"]:
                    raise ValueError("Invalid manufacturer")
            case "type":    
                if value not in ["hot","cold"]:
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
    value = OneOrMore(Word(alphanums)).stopOn(logical_operators)
    value.setParseAction(lambda t: " ".join(t))

    #expression does not handle logical operators
    #example: manufacturer == Kelloggs
    expression = categories + operators + value
    expression.setParseAction(expression_parse)

    #basic query is a series of expressions with logical operators between them
    basic_query = infixNotation(expression, [(logical_operators, 2, opAssoc.LEFT)])


    #adds together expressions with logical operators and additional expressions 
    query_language = OneOrMore(basic_query | lpar + basic_query + rpar) + stringEnd
    
    while not valid_input:
        #initial prompt for input 
        user_input = input("Please enter your query if you need help type \'help\' if you want to quit type \'exit\'\n>>")
        print("\n")#for output readability
        
        #pyparsing uses spaces as a delimiter so I need to add spaces around parentheses
        #does not affect queries that already have spaces around parentheses
        #cause pyparsing handles double spaces 
        if "(" in user_input:
            user_input = user_input.replace('(','( ')
        if ")" in user_input:
            user_input = user_input.replace(')',' )')
            
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
        elif user_input == "exit":
            exit()
        else:
            valid_input = True
            try:
                return query_language.parseString(user_input)[0]
            except Exception as e:
                print(f"Error: {e}")
                valid_input = False
                print("\n")#for output readability
        
    return

#recursive function that formats the query into a list of lists
#with index one containing the expressions which are nested to represent 
#the order of operations and the second index containing the logical operators
def parse_query(input_query, depth, active_index_list, parsed_list):
    active_index_list.append(0)
    expression_list = []
    while active_index_list[depth] < len(input_query):
        if active_index_list[0] >= len(input_query):
            return parsed_list
        elif isinstance(input_query[active_index_list[depth]],list):
            print("in")
            if depth > 0:
                expression_list.append(parse_query(input_query[active_index_list[depth]],depth + 1,active_index_list,parsed_list))
            else:
                parsed_list[0].append(parse_query(input_query[active_index_list[depth]],depth + 1,active_index_list,parsed_list))
            active_index_list.pop()
            active_index_list[depth] += 1
            parsed_list[1].append(input_query[active_index_list[depth]])
            active_index_list[depth] += 1
            print("out")
        else:
            #adds 
            expression = []
            expression.append(input_query[active_index_list[depth]])
            print(parsed_list)
            expression.append(input_query[active_index_list[depth] + 1])
            expression.append(input_query[active_index_list[depth] + 2])
            if depth > 0:
                expression_list.append(expression)
            else:
                parsed_list[0].append(expression)
            try:
                parsed_list[1].append(input_query[active_index_list[depth] + 3])
            except:
                if depth > 0:
                    return expression_list
                return parsed_list

            active_index_list[depth] += 4
    

    return parsed_list

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
user_in = get_input().asList()
print(user_in)
return_list = [[],[]]
active_index_list = []
print(parse_query(user_in,0,active_index_list,return_list))
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