"""=========================================================="""
"""=== Robbie Henderson - Foundations 2 Assignment Part 4 ==="""
"""=========================================================="""
# For part 4 I added 2 lines to the "deal with new node"
# function which recognise the diagonalise JSON operator
# and run my created diagnoalise function with the 3 arguments
#
# I also added the diagonalise function which takes 3 
# checks if the first 2 are functions
# builds all 3 from JSON to python objects
#
# The domain of the first function (x) is then taken and each
# element of this domain has the first function applied to it
# and the result then is applied to x again. The reusult is y
#
# If y is undefined then a tuple is made of (x, V3)
# This is the default entry
#
# Otherwise:
# The second function is applied to y and if defined, 
# then a tuple is created using (x, y)
#
# Once all elements of the domain of function 1 have been 
# used in this way, all the reuslting tuples are added to a
# set which as a set of tuples is a function, and is returned
#
# I also added a is_function2, which is essentially a 
# is_function but takes in a function to test rather than 
# a function in JSON form.  This allowed me to test the left
# hand side of the pairs in v1 to see whether they are functions
#
# Answers to questions will be in accomanying report in: 
# "answers-to-questions.txt"
"""========================================================="""
#CHARACTER ENCODING INFO
#ALLOWS USE OF '#' WITHOUT ANGRY ERROR MESSAGES
# coding: utf-8
"""========================================================="""

#IMPORT JSON LIBRARY
import json
#GLOBAL STORAGE OF ALL PARSED VARIABLES
variable_dict={}


#*********************************
#*********************************
#*** START OF PART 4 FUNCTIONS ***
#*********************************
#*********************************

def diagonalize(v1, v2, v3): #diagonalisation happens here
    #build three arguments
    v1 = is_function(v1) 
    v2 = is_function(v2)
    v3 = build_argument(v3) 

    #check if v1 and v2 are functions
    if v1 == None: #if v1 is not, inform user
	return "argument 1 must be a function"
    if v2 == None: #if v2 is not inform user
	return "argument 2 must be a function"

    newfunction = [] #list of all created tuples for the final function
    domv1 = domain(v1) #get domain of v1

    for x in domv1: #for each element of the left hand side of v1...
	#ensure v1 applied to current element is a function
	if is_function2(apply_function(v1, x)) == 1:
	    y = apply_function(apply_function(v1, x), x) #apply v1 to the result of applying v1 to current element "x" in the domain
	
	    left = x #left of new tuple of new function F is the current member of the domain of v1
	    if not isinstance(y, str):
	    	right = apply_function(v2, y) #right of tuple of new function is the previous result applied to v2

	    	#check if result was undefined
	    	if not isinstance(right, str):
		    newfunction.append(tuple([left,right])) #if defined create new tuple with left and right where right is v2(v1(x)(x))
		    #otherwise the tuple is not added
	    #if v1(x)(x) is not defined then add a tuple of (x, v3) to the new function
	    else:
	    	newfunction.append(tuple([x,v3])) #if not then tuple with left and v3

    return frozenset(newfunction) #return function (set of new tuples)

#*********************************
#*********************************
#**** END OF PART 4 FUNCTIONS ****
#*********************************
#*********************************

#*********************************
#*********************************
#*** START OF PART 3 FUNCTIONS ***
#*********************************
#*********************************

#builds a set or tuple from json data 
#to avoid repeated code in parser
def build_argument(x):
    if isinstance(x, int):
        # if int, return int value
        return x
    #if x contains a reference to a variable...
    elif "variable" in x:
        #check if the variable has been parsed
        #return it if it has
        if x["variable"] in variable_dict:
            return variable_dict[x["variable"]]
        else:
            #otherwise return undefined
            return "undefined"
    elif "operator" in x:
        #if the data has an operator, then parse accordingly
        return deal_with_new_node(x)


#to test if the expression is a function
def is_function(x):
    #the following code essentailly builds the expression
    #in an almost identiacal way to above
    #but will not build an int, int cannot be function
    if "variable" in x:
        if x["variable"] in variable_dict:
            function_to_test = variable_dict[x["variable"]]
        else:
            return "undefined"
    elif "operator" in x:
        function_to_test = deal_with_new_node(x)
    elif isinstance(x, int):
        return None
    #test if expression is set
    if isinstance(function_to_test, frozenset):
        #initialize test variables
        correct_tuple_count = 0
        already_seen = []
        #for each element of the set function
        for current in function_to_test:
            #if tuple and length 2 then add to already seen and count as correct
            if isinstance(current, tuple) and len(current) == 2 and not current[0] in already_seen:
                correct_tuple_count = correct_tuple_count + 1
                already_seen.append(current[0])
            else:
                return None
        if correct_tuple_count == len(function_to_test):
            #if successfull return function
            return function_to_test
        else:
            #otherwise return nothing
            return None
    else:
        return None


#to test if the expression is a function not usinf JSON data
def is_function2(x):
    function_to_test = x
    #test if expression is set
    if isinstance(function_to_test, frozenset):
        #initialize test variables
        correct_tuple_count = 0
        already_seen = []
        #for each element of the set function
        for current in function_to_test:
            #if tuple and length 2 then add to already seen and count as correct
            if isinstance(current, tuple) and len(current) == 2 and not current[0] in already_seen:
                correct_tuple_count = correct_tuple_count + 1
                already_seen.append(current[0])
            else:
                return 0
        if correct_tuple_count == len(function_to_test):
            #if successfull return 1
            return 1
        else:
            #otherwise return 0
            return 0
    else:
        return 0

#function to apply function
def apply_function(function, right):
    argument = build_argument(right) #builds the argument to the function
    for x in function: #for each tuple in the function
        if x[0] == argument: #if the argument is on the left
            return x[1] #return the right
    return "undefined in function" #if not found return undefined message


#return the set of the domain of the function
def domain(function):
    domain_list = [] #empty domain list
    for x in function: #for each tuple in function
        domain_list.append(x[0]) #add to end of domain list, the left of the tuple
    return frozenset(domain_list) # return set of the domain list


#return the set of the range of the function
def function_range(function):
    range_list = [] #list of range elements
    for x in function: # for each in the function
        range_list.append(x[1]) #add end of tuple to list
    return frozenset(range_list) #return set of range list


#inverts each tuple in the function
def function_inverse(function):
    inverse_list = [] #inverted tuple list
    for x in function:
        inverse_list.append(tuple([x[1], x[0]])) #add a new tuple of the original backwards to the tuple list
    return frozenset(inverse_list)


#set union method
def set_union(setA, setB):
    if isinstance(setA, frozenset) and isinstance(setB, frozenset): #if both arguments are sets
        return setA.union(setB) #return the union of arguments
    else: # otherwise return input not sets
        return "input not sets"


#set intersection method
def set_intersection(setA, setB):
    if isinstance(setA, frozenset) and isinstance(setB, frozenset): #if both arguments are sets
        return setA.intersection(setB) #return the intersection of arguments
    else: # otherwise return input not sets
        return "input not sets"


#set difference method
def set_difference(setA, setB):
    if isinstance(setA, frozenset) and isinstance(setB, frozenset): #if both arguments are sets
        return setA.difference(setB) #return the difference of arguments
    else: # otherwise return input not sets
        return "input not sets"


#test if function is injective
def injective(function):
    #create empty list for seen elements
    already_seen = []
    #for each element of set
    for current in function:
        #if output of element has been seen
        if current[1] in already_seen:
            #return 0 for false
            return 0
        else:
            #add to list
            already_seen.append(current[1])
    return 1
#*********************************
#*********************************
#**** END OF PART 3 FUNCTIONS ****
#*********************************
#*********************************

"""======================================"""
"""=== RECURSIVE PARSING OF OPERATORS ==="""
"""====== WHERE THE MAGIC HAPPENS ======="""
"""======================================"""
def deal_with_new_node(argument):
    #takes in the list of arguments ascociated with the argument key
    argv = argument["arguments"]
    #checks operastor
    #-if the arguments have to be placed in a set
    if argument["operator"] == "set":
        """========================="""
        """========== SET =========="""
        """========================="""
        #if the arguments are to be placed in a set...
        #create new empty list
        newset = set([])
        for x in argv:
            #for each element of the arguments list
            if isinstance(x, int):
                #if integer, add to set
                newset.add(x)
            elif "operator" in x:
                #if operator exists then recurse this function with x
                if deal_with_new_node(x) == "undefined":
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
                else:
                    newset.add(deal_with_new_node(x))
            elif "variable" in x:
                #if variable required then get variable from parsed dict
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        #returning undefined to allow failed variables to be displayed
                        return "undefined"
                    else:
                        #if the variable has been stored, add to list
                        newset.add(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
        #create and return set from list of data
        new_frozenset = frozenset(newset)
        if "undefined" in new_frozenset:
            #returning undefined to allow failed variables to be displayed
            return undefined
        else:
            return new_frozenset
        #fallback result
        return 0

    elif argument["operator"] == "tuple":
        """========================="""
        """========= TUPLE ========="""
        """========================="""
        #tuple required - time for tuples
        #create list for tuple creation
        tuple_contents = []
        #for each part of the argument
        for x in argv:
            #if int add to list
            if isinstance(x, int):
		        tuple_contents.append(x)
            #if the argument has an operator, carry out operation by recursion
            elif "operator" in x:
                if deal_with_new_node(x) == "undefined":
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
                else:
                    tuple_contents.append(deal_with_new_node(x))
            #if the arg is a vriable , find variable and and to list
            elif "variable" in x:
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        #returning undefined to allow failed variables to be displayed
                        return "undefined"
                    else:
                        tuple_contents.append(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
        """========================="""
        """===== FUN EXTENSION ====="""
        """========================="""
        #if tuple is too small return error tuple and print error
        if len(tuple_contents)==1:
            print 'error at:'
            print argv
            print('tuple cannot be of length 1')
            return tuple(["tuple cannot be","of length one"])
        else:
            new_tuple = tuple(tuple_contents)
            return new_tuple
        #fallback result
        return 0
    
    #if any arguments are found using the same methods as before
    #they are added to the end of a list
    #the arguments are compared and if equal 1 is returned
    elif argument["operator"] == "equal":
        """========================="""
        """======== EQUALITY ======="""
        """========================="""
        comparisons = []
        for x in argv:
            if isinstance(x, int):
                comparisons.append(x)
            elif "operator" in x:
                if deal_with_new_node(x) == "undefined":
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
                else:
                    comparisons.append(deal_with_new_node(x))
            elif "variable" in x:
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        #returning undefined to allow failed variables to be displayed
                        return "undefined"
                    comparisons.append(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
        if comparisons[0] == comparisons[1]:
            if comparisons [0] == "undefined" or comparisons[1] == "undefined":
                #returning undefined to allow failed variables to be displayed
                return "undefined"
            else:
                return 1
        #fallback result
        return 0

    #if any arguments are found using the same methods as before
    #they are added to the end of a list
    #the arguments are compared and first is in second 1 is returned   
    elif argument["operator"] == "member":
        """========================="""
        """========= MEMBER ========"""
        """========================="""
        comparisons = []
        for x in argv:
            if isinstance(x, int):
                comparisons.append(x)
            elif "operator" in x:
                if deal_with_new_node(x) == "undefined":
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
                comparisons.append(deal_with_new_node(x))
            elif "variable" in x:
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        #returning undefined to allow failed variables to be displayed
                        return "undefined"
                    comparisons.append(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
        if comparisons[0] in comparisons[1]:
            #the integers cannot have any members - must fail
            if not isinstance(comparisons[1],int):
                if comparisons [0] == "undefined" or comparisons[1] == "undefined":
                    #returning undefined to allow failed variables to be displayed
                    return "undefined"
                else:
                    return 1
            else:
                return '0 - int cannot have members'
        #fallback result
        return 0

#*********************************
#*********************************
#**** START OF PART 3 PARSING ****
#*********************************
#*********************************
	#calculate is-function
    elif argument["operator"] == "is-function":
        success = is_function(argv[0]) #run is function
        if not success == None: #if a function is returned then the input is a function
            return 1 #return 1
        else: #otherwise failed
            return 0 #return 0 or false

	#calculate apply-function
    elif argument["operator"] == "apply-function":
        funct = is_function(argv[0]) #run is function to ensure a function is being applied to and get the built function to work on
        if not funct == None: #run if input is function
            return apply_function(funct, argv[1]) #apply function on the returned fuinction with the second argument
        else:
            return "undefined" #if not a function then return undefined

	#calculate domain of function
    elif argument["operator"] == "domain":
        funct = is_function(argv[0]) #run is function to ensure a function is being applied to and get the built function to work on
        if not funct == None: #run if input is function
            return domain(funct) #return the result of the domain method applied to the function
        else:
            return "undefined" #if not a function then return undefined

	#calculate range of function
    elif argument["operator"] == "range":
        funct = is_function(argv[0]) #run is function to ensure a function is being applied to and get the built function to work on
        if not funct == None: #run if input is function
            return function_range(funct) #return the result of the range method applied to the function
        else:
            return "undefined" #if not a function then return undefined

	#calculate intersection of 2 sets
    elif argument["operator"] == "intersection":
        sets = argument["arguments"]
        setA = build_argument(sets[0]) #build the set from first argument
        setB = build_argument(sets[1]) #build the set from second argument
        return set_intersection(setA, setB) #return the difference of the 2 sets

	#calculate union of 2 sets
    elif argument["operator"] == "union":
        sets = argument["arguments"]
        setA = build_argument(sets[0]) #build the set from first argument
        setB = build_argument(sets[1]) #build the set from second argument
        return set_union(setA, setB) #return the difference of the 2 sets

	#calculate difference of 2 sets
    elif argument["operator"] == "set-difference":
        sets = argument["arguments"]
        setA = build_argument(sets[0]) #build the set from first argument
        setB = build_argument(sets[1]) #build the set from second argument
        return set_difference(setA, setB) #return the difference of the 2 sets

	#calculate inverse of a function
    elif argument["operator"] == "inverse":
        funct = is_function(argv[0]) #run is function to ensure a function is being applied to and get the built function to work on
        if not funct == None: #run if input is function
            return function_inverse(funct) #return the inverse of the input function
        else:
            return "undefined" #if not a function then return undefined
            
	#calculate if a function is injective
    elif argument["operator"] == "is-injective":
        funct = is_function(argv[0]) #run is function to ensure a function is being applied to and get the built function to work on
        if not funct == None: #run if input is function
            return injective(funct) #return 1 if the function is injective, 0 otherwise
        else:
            return "undefined" #if not a function then return undefined

    #diagonalize
    elif argument["operator"] == "diagonalize":
	#run diagaonalisation with the 3 provided variables
	return diagonalize(argv[0], argv[1], argv[2])


#*********************************
#*********************************
#***** END OF PART 3 PARSING *****
#*********************************
#*********************************
    else:
        return "not seen this operator before..."


"""===============================
INITIALIZE PARSING OF JSON FILE
==============================="""
#having 2 seperate parsing functions allows the program
#to ignore the first equals which is always assigning 
#a value to variable, rather than equivalence
def parse_json(current):
    #if current operator is equal
    #parse the expression
    if current["operator"]=="equal":
        #get arguments and variable name from dict with relevant keys
        argv = current["arguments"]
        var = argv[0]["variable"]
        #if the argument is an integer, assign value
        if isinstance(argv[1], int):
            variable_dict[var] = argv[1]
        #incase of variable assignment to variable
        elif "variable" in argv[1]:
			#check if variable exists, assign if so
			if argv[1]["variable"] in variable_dict:
				variable_dict[var] = variable_dict[argv[1]["variable"]]
			#otherwise assign undefined
			else:
				variable_dict[var] = "undefined"
        #otherwise, deal with more complex operators etc
        #in new node function
        else:
            #assign value to variable as key in dict
            variable_dict[var] = deal_with_new_node(argv[1])

    #write all variables and value to file f opened in main
    f.write (var + " = ")			
    write_out(variable_dict[var])
    f.write(';\n')


"""====================================
METHOD TO CARRY OUT RECURSIVE PRINTING
===================================="""
def output(out):
    #counter is used to tell if comma is required
    counter = 0
    #for every member of the set/tuple - x
    for x in out:

        #if x is a set, print releavnt brackets
        if isinstance(x,frozenset):
            #print comma if not in first position
            if counter != 0:
                f.write(',')
            f.write('{')
            #call this function to print x
            output(x)
            f.write('}')
            counter = counter+1

        #if x is a tuple, print releavnt brackets
        elif isinstance(x,tuple):
            #print comma if not in first position
            if counter != 0:
                f.write(',')
            f.write('(')
            #call this function to print x
            output(x)
            f.write (')')
            counter = counter+1

        #if x is a string then simply print the integer
        elif isinstance(x,str):
            #print comma if not in first position
            if counter != 0:
                f.write(',')
            f.write(x)
            counter = counter+1

        #if int, print int
        elif isinstance(x,int):
            #print comma if not in first position
            if counter != 0:
                f.write(',')
            f.write('%d' % x)
            counter = counter+1


"""===============================
METHOD TO INITIALIZE PRINTING
==============================="""
def write_out(to_write):
    # if current member is int, write to file
    if isinstance(to_write, int):
        f.write('%d' % to_write)
        
    # if string etc undefined, print
    if isinstance(to_write, str):
        f.write(to_write)
        
    #if set, print relevant brackets then reccurse on contained set
    elif isinstance(to_write, frozenset):
        f.write('{')
        #run output for set x
        output(to_write)
        f.write('}')
        
    #if tuple, print relevant brackets then recurse on contained tuple
    elif isinstance(to_write,tuple):
        f.write('(')
        #run output for tuple x
        output(to_write)
        f.write (')')


"""=====================
 MAIN PROGRAM RUNS HERE
====================="""
#name in nd out files
#in couldnt be used as is already used in python
#inwards is basically the same....
inwards = "input.json"
outwards = "output.txt"

#open output.txt for writing evaluated expressions
f = open(outwards, 'w+')

#open json file for reading
json_file = open(inwards, 'r')

#try to open json file
#print bad output if failed
try:
	#use imported json library to load json into dict input_data
	input_data = json.load(json_file)
	#for every member of the list with key 'statement-list' in the loaded dict
	for x in input_data["statement-list"]:
		#parse the current member of the list
		parse_json(x)
except ValueError:
	f.write("BAD INPUT")

#inform user where output is going - just in case...
print '\nloaded \''+inwards+'\' as input'
print 'output to \''+outwards+'\' \n'

#close opened files
f.close()
print '\nclosed \''+inwards+'\' - input file'
json_file.close()
print 'closed \''+outwards+'\' output file\n'
