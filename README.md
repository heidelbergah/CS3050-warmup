# CS3050 Warmup Collaborative Project
### Names Here

## Dataset
We used the dataset "[80 Cereals](https://www.kaggle.com/datasets/crawford/80-cereals)" from Kaggle.com. Contains the specifications and nutrition data for 80 different popular cereal products. We excluded many columns from the original dataset for brevity.

## Query Language
Each query in our language is made of a series of conditions. A condition is defined with the following:
    - Type: The column of the dataset to be scrutinized
    - Operator: The type of comparison being made (Greater Than, Not Equal To, etc.)
    - Value: Value that the type's appropriate field will be compared to
Conditions are attached to the same query through Logical Operators

## Keywords
Types:
    - manufacturer: Company/Firm that produces the product
    - type: Cereal temperature, either "cold" or "hot"
    - rating: Consumer Rating of the product
    - shelf: Physical sotre shelf location; 1, 2, or 3
    - potassium: Potassium content in grams

Operators:
    - <: Less Than
    - <=: Less Than or Equal To
    - >: Greater Than
    - >=: Greater Than or Equal To
    - ==: Equal To
    - !: Negative Operator
    - (): Grouping Operator

Values:
    - manufacturer -> (str)
    - type -> (str); "cold" or "hot"
    - rating -> (int); range 1-100
    - shelf -> (int); 1, 2, or 3
    - potassium -> (int); >= 0

Logical Operators:
    - and: AND Operator
    - or: OR Operator

## Example Queries

## Functional Interface

## Code Functions