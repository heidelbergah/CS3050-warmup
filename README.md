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
    
    shelf: Physical sotre shelf location; 1, 2, or 3
    
    potassium: Potassium content in grams

Operators:
    
    <: Less Than
    
    <=: Less Than or Equal To
    
    >: Greater Than
    
    >=: Greater Than or Equal To
    
    ==: Equal To
    
    !: Negative Operator
    
    (): Grouping Operator

Values:
    
    manufacturer -> (str)
    
    type -> (str); "cold" or "hot"
    
    rating -> (int); range 1-100
    
    shelf -> (int); 1, 2, or 3
    
    potassium -> (int); >= 0

Logical Operators:
    
    and: AND Operator
    
    or: OR Operator

## Example Queries
Example of a simple query:

    "manufacturer == General Mills"

Example of a query with two conditions

    "manufacturer == General Mills and potassium > 0"

Example of a grouped query

    "(manufacturer == Kelloggs and rating > 90) or shelf == 1"


## Functional Interface
The functional interface allows users to enter a query that will be parsed and sent to the Firestore database.

Users are able to enter one complete query with an unlimited number of conditions as the input. 

Returned data entries are printed as a list of appropriate Cereal Names in the program's output.

The user is able to view a list of available operators and example queries by using the 'help' command. 

The 'exit' command terminates the program when the user is finished

## Code Functions
Firebase Connection (admin.py):

    establish_connection():

    parse_json_data(json_file):

    push_data(db, data, collection_name):

    collection_exists(db, collection_name):

    delete_collection(db, collection_name):

    initialize_database(collection_name="cereal_data"):

Admin (admin.py):

Query (query.py):

    get_input():

        expression_parse(tokens):

    parse_query(input_query, depth, active_index_list, parsed_list):

    retrieve_query(parsed_input):

    execute_query(query):

    fancy_print(cereals):
