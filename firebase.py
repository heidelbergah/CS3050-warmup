from google.cloud import firestore
from admin import establish_connection

def retrieve_query(parsed_input):
    """
    Executes a query on the Firestore database based on the parsed input.

    This function takes the parsed query structure and converts it into Firestore-compatible 
    filters. Each expression in the parsed input is translated into a Firestore 
    query clause, and the results are retrieved and returned as a list of cereal names.

    Args:
        parsed_input (list): A structured list containing expressions and logical operators.
            - parsed_input[0]: List of expressions, where each expression is a list 
              in the format [param, comparator, value].
            - parsed_input[1]: List of logical operators (e.g., ['and', 'or']).

    Returns:
        list: A list of cereal names that match the query criteria.
    """
    expressions = parsed_input[0]

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
            case "american":
                value = "A"
            case "general":
                value = "G"
            case "kelloggs":
                value = "K"
            case "nabisco":
                value = "N"
            case "post":
                value = "P"
            case "quaker":
                value = "Q"
            case "ralston":
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

