#
# Q1

# Variable: A storage location identified by its name, containing some value.
# Question: Assign a value of 10 to variable a and 20 to variable b
# Question: Store the result of a + b in a variable c and print it. What is the result of a + b?

a = 10 
b = 20

c = a + b 
c

# Q2 

# Question: How do you remove the empty spaces in front of and behind the string s?

# print some string 
s = '  Some string '
print(s)

print(s.strip())


# Q3 

# Data Structures are ways of representing data, each has its own pros and cons and places that they are the right fit.
## List: A collection of elements that can be accessed by knowing the location (aka index) of the element
l = [1, 2, 3, 4]

print(l[0]) 
print(l[1])
print(l[2])
print(l[3])

#Q4 

## Dictionary: A collection of key-value pairs, where each key is mapped to a value using a hash function. Provides fast data retrieval based on keys.
d = {'a': 1, 'b': 2}
d

print(d.get('a'))
print(d.get('b'))

# Q5

## Set: A collection of unique elements that do not allow duplicates
my_set = set()
my_set.add(10)
my_set.add(10)
my_set.add(10)

print(my_set) # only returns 10 since set keeps unique values 

my_set = set()
my_set.add(10)
my_set.add(8)
my_set.add(15)

print(my_set) # this returns the list of the different values added 

#Q6 

## Tuple: A collection of immutable (non-changeable) elements, tuples retain their order once created.
my_tuple = (1, 'hello', 3.14)

print(my_tuple)

# Question: How do you access the elements in index 0 and 1 of my_tuple?
print(my_tuple[0])  # Output: 1
print(my_tuple[1])  # Output: 'hello'


# Q7

## Counting occurrences of an element
count_tuple = (1, 2, 3, 1, 1, 2)

# Question: How many times does the number 1 appear in count_tuple?
print(count_tuple.count(1))  # Output: 3

# Q8

## Finding the index of an element

# Question: What is the index of the first occurrence of the number 2 in count_tuple?
print(count_tuple.index(2))  # Output: 1

# Q9

# Loop allows a specific chunk of code to be repeated a certain number of times
# Example: We can use a loop to print numbers 0 through 10
for i in range(11):
    print(i)

# Q11

## We can loop through our data structures as shown below
# Question: How do you loop through a list and print its elements?
for elt in l:
    print(elt)  # Or any operation you may want to do
## We can do a similar loop for tuples and sets

# Q12

## Dictionary loop
# Question: How do you loop through a dictionary and print its keys and values?
for k, v in d.items():
    print(f'Key: {k}, Value: {v}')  # Print key and values in dictionary


# Q13

## Comprehension is a shorthand way of writing a loop
## For example, we can use the below to multiply every element in list l with 2
print([elt*2 for elt in l])

# Q14

# Functions: A block of code that can be re-used as needed. This allows for us to have logic defined in one place, making it easy to maintain and use.
## For example, let's create a simple function that takes a list as an input and returns another list whose values are greater than 3

def gt_three(input_list):
    return [elt for elt in input_list if elt > 3]
## NOTE: we use list comprehension with filtering in the above function

list_1 = [1, 2, 3, 4, 5, 6]
# Question: How do you use the gt_three function to filter elements greater than 3 from list_1?
print(gt_three(list_1))  # Will print [4, 5, 6]

list_2 = [1, 2, 3, 1, 1, 1]
# Question: What will be the output of gt_three(list_2)?
print(gt_three(list_2))  # Will print []

# Q15 

# Classes and Objects
# Think of a class as a blueprint and objects as things created based on that blueprint
# You can define classes in Python as shown below

class DataExtractor:

    def __init__(self, some_value):
        self.some_value = some_value

    def get_connection(self):
        # Some logic
        # some_value is accessible using self.some_value
        pass

    def close_connection(self):
        # Some logic
        # some_value is accessible using self.some_value
        pass

# Question: How do you create a DataExtractor object and print its some_value attribute?
de_object = DataExtractor(10)
print(de_object.some_value)  # Will print 10

# Q16

# Libraries are code that can be reused.

# Python comes with some standard libraries to do common operations, 
# such as the datetime library to work with time (although there are better libraries)
from datetime import datetime  # You can import library or your code from another file with the import statement

# Question: How do you print the current date in the format 'YYYY MM DD'?
print(datetime.now().strftime('%Y %m %d'))  # We can use multiple such methods 

# Q17

# Exception handling: When an error occurs, we need our code to gracefully handle it without just stopping. 
## Here is how we can handle errors when the program is running
try:
    # Code that might raise an exception
    pass
except Exception as e: 
    # Code that runs if the exception occurs
    pass
else:
    # Code that runs if no exception occurs
    pass
finally:
    # Code that always runs, regardless of exceptions
    pass

## For example, let's consider exception handling on accessing an element that is not present in a list l
l = [1, 2, 3, 4, 5]

index = 10
try:
    # Attempt to access an element at an invalid index
    element = l[index]
    print(f"Element at index {index} is {element}")
except IndexError:
    print(f"Error: Index {index} is out of range for the list.")
finally:
    print("Execution completed.")
# NOTE: in the except block its preferred to specify the exact erro/exception that you want to handle
