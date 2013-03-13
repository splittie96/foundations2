"""========================================================"""
"""== Robbie Henderson - Foundations 2 Assignment Part 2 =="""
"""========================================================"""

#CHARACTER ENCODING INFO
#ALLOWS USE OF '#' WITHOUT ANGRY ERROR MESSAGES
# coding: utf-8

#IMPORT JSON LIBRARY
import json
#GLOBAL DICTIONARY OF ALL PARSED VARIABLES
variable_dict={}

def is_function(x):
    if "variable" in x:
        if x["variable"] in variable_dict:
            function_to_test = variable_dict[x["variable"]]
        else:
            return "undefined"
    elif "operator" in x:
        function_to_test = deal_with_new_node(x)
    elif isinstance(x, int):
        return 0
    if isinstance(function_to_test, frozenset):
        correct_tuple_count = 0
        already_seen = []
        for current in function_to_test:
            if isinstance(current, tuple) and len(current) == 2 and not current[0] in already_seen:
                correct_tuple_count = correct_tuple_count + 1
                already_seen.append(current[0])
        if correct_tuple_count == len(function_to_test):
            return 1
        else:
            return 0
    else:
        return 0

def apply_function(left, right):
    if "variable" in left:
        if left["variable"] in variable_dict:
            function = variable_dict[left["variable"]]
        else:
            return "undefined"
    elif "operator" in left:
        function = deal_with_new_node(left)

    if isinstance(right, int):
        argument = right
    elif "variable" in right:
        if right["variable"] in variable_dict:
            argument = variable_dict[right["variable"]]
        else:
            return "undefined"
    elif "operator" in right:
        argument = deal_with_new_node(right)

    for x in function:
        if x[0] == argument:
            return x[1]
    return "undefined"


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


    elif argument["operator"] == "is-function":
        return is_function(argv[0])


    elif argument["operator"] == "apply-function":
        if is_function(argv[0]) == 1:
            return apply_function(argv[0], argv[1])
        else:
            return "undefined"

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
f = open(outwards, 'w')

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
