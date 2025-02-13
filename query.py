from pyparsing import *
from firebase import retrieve_query

def get_input():
    """
    Prompts the user for a query and parses it using the defined query language grammar.

    The query language supports logical operators (`and`, `or`), comparison operators 
    (`==`, `<`, `>`, `<=`, `>=`, `!=`), and predefined categories 
    (`manufacturer`, `type`, `rating`, `shelf`, `potassium`). The user can also type `help` 
    to get a description of the query language or `exit` to quit the program.

    Returns:
        str: The parsed query as a list if valid, or the string "exit" if the user chooses to quit.
        Raises a ValueError for invalid query elements.

    Exceptions:
        Prints an error message if the input is invalid and prompts the user to try again.
    """
    # input starts as False
    valid_input = False
    
    #defines the categories that can be used in a query always at the start of 
    #an expression
    categories = (Literal("manufacturer") | Literal("type") | Literal("shelf") | 
                  Literal("potassium") | Literal("rating"))

    #define acceptable operators
    operators = (Literal("<=") | Literal(">=") | Literal("<") | 
                 Literal(">")  | Literal("!=") | Literal("=="))
    
    #parse action for expressions to create accurate error messages
    def expression_parse(loc,tokens):
        category, operator, value = tokens
        error_location = loc + len(category)  + len(operator) + 2
        match category:
            case "manufacturer":
                if value.lower() not in ["american home food products","general mills",
                            "kelloggs","nabisco","post","quaker oats",
                            "ralston purina"]:
                    raise ParseException("Invalid manufacturer input",error_location)
                elif operator != "==" and operator != "!=":
                    error_location = loc + len(category) + 1
                    raise ParseException("Invalid operator for manufacturer expected ['==' or '!=']",
                                         error_location)
            case "type":    
                if value.lower() not in ["hot","cold"]:
                    raise ParseException("Invalid type input",error_location)
                elif operator != "==" and operator != "!=":
                    error_location = loc + len(category) + 1
                    raise ParseException("Invalid operator for type expected ['==' or '!=']",
                                         error_location)
            case "rating":
                #needed to try and convert the string to an int 
                # and then raise errors outside the try otherwise it just goes the 
                # the except portion 
                try:
                    int(value)    
                except Exception as e:
                    if "invalid literal for int()" in e:
                        raise ParseException(f"Invalid {category} input. Input an integer",
                                             error_location)
                if int(value) not in range(101):
                    raise ParseException(f"Invalid {category} input, not in range 0 - 100",
                                         error_location)
            case "shelf":
                try:
                    int(value)    
                except Exception as e:
                    if "invalid literal for int()" in e:
                        raise ParseException(f"Invalid {category} input. Input an integer",
                                             error_location)
                if int(value) not in range(1,4):
                    raise ParseException(f"Invalid {category} input, not in range 1 - 3",
                                         error_location)
            case "potassium": 
                try:
                    int(value)    
                except Exception as e:
                    if "invalid literal for int()" in e:
                        raise ParseException(f"Invalid {category} input. Input an integer",
                                             error_location)
                if int(value) not in range(1001):
                    raise ParseException(f"Invalid {category} input, not in range 0 - 100",
                                         error_location)
        return tokens
    
    #value can take a string or integer and will stop when it reaches a logical operator
    #the list of strings if it was more than one is then joined together
    value = OneOrMore(Word(alphanums)).stopOn("and" | categories | stringEnd)
    value.setParseAction(lambda x: " ".join(x))

    #expression does not handle logical operators
    #example: manufacturer == Kelloggs
    expression = categories + operators + value
    expression.setParseAction(expression_parse)

    #basic query is a series of expressions with logical operators between them
    query = (expression + ZeroOrMore(Word(alphas) + expression)) + stringEnd


    while not valid_input:
        #initial prompt for input 
        user_input = input("Please enter your query if you need help type 'help'"  + 
                           " if you want to quit type \'exit\'\n>>").lower()
        print("\n")#for output readability
        
        #pyparsing uses spaces as a delimiter so I need to add spaces around parentheses
        #does not affect queries that already have spaces around parentheses
        #cause pyparsing handles double spaces 
        if "(" in user_input:
            user_input = user_input.replace('(','')
        if ")" in user_input:
            user_input = user_input.replace(')','')
            
        if user_input.lower().replace(" ","") ==  "exit":
            print("Exiting the Cereal Query Program. Goodbye!")
            return user_input.lower().replace(" ","")
        elif user_input.lower() == "help":
            print("Query Language:\nmanufacuter: manufacturer of the cereal\n" + 
                  "type: type of cereal, cold or hot\n" + 
                  "rating: rating of cereal 0-100\n" + 
                  "shelf: shelf from the floor 1,2,3\n" + 
                  "potassium: amount of potassium in cereal\n" + 
                  "and: and\n<: less than\n<=: less than or equal to\n" + 
                  ">: greater than\n>=: greater than or equal to\n" + 
                  "==: is or equal to\n" + 
                  "!=: is not equal to operator\n\nExamples:\n" + 
                  "manufacuter == Kelloggs and potassium > 0\n" + 
                  "shelf == 3 and potassium > 0\n" + 
                  "Queries are case sensitive\n")

        else:
            valid_input = True
            try:
                valid_query = query.parseString(user_input).as_list()
                #makes sure that the list returned is not just a list containing 
                #only a list at index 0 and nothing else
                if isinstance(valid_query[0],list):
                    return valid_query[0]
                else:
                    return valid_query
            except ParseException as pe:
                print(pe)
                valid_input = False
                print("\n") # for output readability
        
    return

#recursive function that formats the query into a list of lists
#with index one containing the expressions which are nested to represent 
#the order of operations and the second index containing the logical operators
def parse_query(input_query, depth, active_index_list, parsed_list):
    """
    Recursively parses the input query into a structured list format, 
    separating expressions and logical operators.

    This function is designed to handle nested queries with parentheses and preserve the logical 
    structure of the query for easier processing later.

    Args:
        input_query (list): The parsed query input as a list of tokens.
        depth (int): The current depth of recursion (tracks nested parentheses).
        active_index_list (list): Tracks the current index in the input query at each depth level.
        parsed_list (list): A list that will store the parsed query structure. 
            parsed_list[0]: List of expressions (e.g., ['manufacturer', '==', 'Kelloggs'])
            parsed_list[1]: List of logical operators (e.g., ['and', 'or'])

    Returns:
        list: A structured list of parsed expressions and logical operators, preserving the order 
        of operations.

    Exceptions:
        Catches and handles indexing errors for malformed queries.
    """
    active_index_list.append(0)
    expression_list = []
    while active_index_list[depth] < len(input_query):
        #active_index_list[0] is the active index of the original input_query list
        if active_index_list[0] >= len(input_query):
            return parsed_list
        #if the current index is a list then it will call parse_query using 
        #input_query[active_index_list[depth]] as the new input_query
        elif isinstance(input_query[active_index_list[depth]],list):
            if depth > 0:
                expression_list.append(parse_query(input_query[active_index_list[depth]],depth + 1,
                                                   active_index_list,parsed_list))
            else:
                parsed_list[0].append(parse_query(input_query[active_index_list[depth]],depth + 1,
                                                  active_index_list,parsed_list))
            active_index_list.pop()
            active_index_list[depth] += 1
            parsed_list[1].append(input_query[active_index_list[depth]])
            active_index_list[depth] += 1
        #if the current index is a string then it can assume that the string 
        #is a category and that the next two indexes are a comparator and a value
        else:
            #adds 
            expression = []
            expression.append(input_query[active_index_list[depth]])
            expression.append(input_query[active_index_list[depth] + 1])
            expression.append(input_query[active_index_list[depth] + 2])
            #if the depth > 0(so not using the original input_query) then it will append the 
            #expression to the expression_list because that is used to handle nested statments 
            #in the parsed_list
            if depth > 0:
                expression_list.append(expression)
            else:
                parsed_list[0].append(expression)
            
            #trys and if there is a next index in the input_query then it will append the logical 
            #operator to the parsed_list[1]
            try:
                parsed_list[1].append(input_query[active_index_list[depth] + 3])
            except:
                if depth > 0:
                    return expression_list
                else: 
                    return parsed_list

            active_index_list[depth] += 4
    return parsed_list


def execute_query(query):
    """
    Parses, executes, and prints the results of the user's query.

    This function takes a parsed query list, processes it using `parse_query()`, 
    and passes the structured query to `retrieve_query()` to fetch results from the database. 
    It then calls `fancy_print()` to display the results.

    Args:
        query (ParseResults): The query input parsed by `get_input()`. It is expected to be in 
                              the format returned by `pyparsing`.

    Returns:
        None. Prints the results of the query to the console.
    """
    return_list = [[],[]]
    active_index_list = []
    depth = 0 # default
    fancy_print(retrieve_query(parse_query(query, depth, active_index_list, return_list)))


def fancy_print(cereals):
    """
    Displays the query results in a user-friendly format.

    This function takes a list of cereal names and prints each name on a new line.
    If the list is empty, it informs the user that no cereals meet the query criteria.

    Args:
        cereals (list): A list of cereal names retrieved from the database.

    Returns:
        None. Prints the list of cereals to the console.
    """
    # printing results to counsole
    if len(cereals) == 0:
        print("No cereals meet these requirements!")
    for cereal in cereals:
        print(f"- {cereal}")
    print("\n") # Two empty lines


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
        if user_query == "exit":
            break
        try:
            # Execute the query and print the results
            execute_query(user_query)
        except Exception as e:
            print(f"An error occurred: {e}")


# Run the program            
if __name__ == "__main__":
    main()

