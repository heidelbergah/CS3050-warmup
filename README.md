# CS3050 Warmup Collaborative Project
### Names Here

## Dataset
We used the dataset "[80 Cereals](https://www.kaggle.com/datasets/crawford/80-cereals)" from Kaggle.com. Contains the specifications and nutrition data for 80 different popular cereal products. We excluded many columns from the original dataset for brevity.

## Query Language
The formatting of the query language closely follows the syntax of logical statements in Python.

Each query in our language is made of a series of conditions. Multiple conditions are attached to the same query through Logical Operators. A condition is defined with the following:
    
    Type: The column of the dataset to be scrutinized
    
    Operator: The type of comparison being made (Greater Than, Not Equal To, etc.)
    
    Value: Value that the type's appropriate field will be compared to

## Keywords
Types:
    
    manufacturer: Company/Firm that produces the product
    
    type: Cereal temperature, either "cold" or "hot"
    
    rating: Consumer Rating of the product
    
    shelf: Physical store shelf location; 1, 2, or 3
    
    potassium: Potassium content in grams

Operators:
    
    <: Less Than
    
    <=: Less Than or Equal To
    
    >: Greater Than
    
    >=: Greater Than or Equal To
    
    ==: Equal To
    
    !=: Not Equal To
    
Values:
    
    manufacturer -> (str)
    
    type -> (str); "cold" or "hot"
    
    rating -> (int); range 1-100
    
    shelf -> (int); 1, 2, or 3
    
    potassium -> (int); >= 0

Logical Operators:
    
    and: AND Operator

## Example Queries
Example of a simple query:

    "manufacturer == General Mills"

Example of a query with two conditions

    "manufacturer == General Mills and potassium > 0"

Example of a grouped query

    "shelf == 2 and rating >= 60"


## Functional Interface
The functional interface allows users to enter a query that will be parsed and sent to the Firestore database.

Users are able to enter one complete query with an unlimited number of conditions as the input. 

Returned data entries are printed as a list of appropriate Cereal Names in the program's output.

The user is able to view a list of available operators and example queries by using the 'help' command. 

The 'exit' command terminates the program when the user is finished

## Code Functions
Firebase Connection (firebase.py):

    retrieve_query(parsed_input):
        * Executes a query on Firestore based on the parsed query structure and retrieves matching cereal data.
        * Params: parsed_input (list); Structured list of expressions and logic operators
        * Returns: return_list (list); A list of cereal names that match the query

Admin (admin.py):
    
    establish_connection():
        * Establishes a connection to the Firebase database using a provided key.
        * Params: None
        * Returns: firestore.client
    
    collection_exists(db, collection_name):
        * Checks if a Firestore collection exists by querying for at least one document.
        * Params: 
            * db (firestore.Client)
            * collection_name (str)
        * Returns:
            * bool; True if the collection has at least one document, False otherwise


    delete_collection(db, collection_name):
        * Deletes all documents in a specified Firestore collection.
        * Params:
            * db (firestore.Client)
            * collection_name (str)
        * Returns: None

    parse_json_data(json_file):
        * Reads and parses data from a JSON file.
        * Params: json_file (str); The appropriate file path
        * Returns:
            * dict, if successful
            * None, if unsuccessful

    push_data(db, data, collection_name):
        * Uploads data to a specified Firestore collection.
        * Params:
            * db (firestore.Client); Firestore client object
            * data (list); The data to upload
            * collection_name (str); Name of the Firestore collection
        * Returns: None

    initialize_database(collection_name="cereal_data"):
        * Initializes the database by reading a JSON file, deleting the existing collection (if present), and uploading new data.
        * Params: collection_name (optional str); Defaults to "cereal_data" if none given
        * Returns: None

Query (query.py):

    get_input():
        * Prompts the user for a query and validates it against a custom query grammar using pyparsing. Supports help and exit commands.
        * Params: None
        * Returns:
            * valid_query (list); The parsed query as a list
            * "exit" (str); if the user wants to quit

    parse_query(input_query, depth, active_index_list, parsed_list):
        * Recursively parses a query into a structured format, separating expressions and logical operators to preserve order of operations.
        * Params: 
            * input_query (list); The parsed query tokens
            * depth (int); Tracked nested parenthesis for recursion
            * active_index_list (list): Tracked current index at each depth
            * parsed_list (list): A structured list to store parsed expressions and local operators.
        * Returns: (list); The structured list representing the parsed query

    execute_query(query):
        * Parses, executes, and prints the results of the user's query.
        * Params: query (list); The parsed query input
        * Returns: None

    fancy_print(cereals):
        * Displays the query results in a user-friendly format.
        * Params: cereals (list); List of retreived cereal names
        * Returns: None
