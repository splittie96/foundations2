#CHARACTER ENCODING INFO
#ALLOWS USE OF '#' WITHOUT ANGRY ERROR MESSAGES
# coding: utf-8

#IMPORT JSON LIBRARY
import json
#GLOBAL DICTIONARY OF ALL PARSED VARIABLES
variable_dict={}

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
        #if the arguments are to be placed in a set...
        newset = set([])
        for x in argv:
            #for each element of the arguments list
            if isinstance(x, int):
                #if integer, add to set
                newset.add(x)
            elif "operator" in x:
                #if operator exists then recurse this function with x
                if deal_with_new_node(x) == "undefined":
                    return "undefined"
                else:
                    newset.add(deal_with_new_node(x))
            elif "variable" in x:
                #if variable required then get variable from parsed dict
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        return "undefined"
                    else:
                        newset.add(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    return "undefined"
        new_frozenset = frozenset(newset)
        if "undefined" in new_frozenset:
            return undefined
        else:
            return new_frozenset

        
    elif argument["operator"] == "tuple":
	tuple_contents = []
        for x in argv:
            if isinstance(x, int):
		        tuple_contents.append(x)
            elif "operator" in x:
                if deal_with_new_node(x) == "undefined":
                    return "undefined"
                else:
                    tuple_contents.append(deal_with_new_node(x))
            elif "variable" in x:
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        return "undefined"
                    tuple_contents.append(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    return "undefined"
        new_tuple = ()
        if len(tuple_contents)==1:
            print 'error at:'
            print argv
            raise Exception ('Tuple cannot be of length 1!')
        else:
            new_tuple = tuple(tuple_contents)
        return new_tuple
    
    elif argument["operator"] == "equal":
        comparisons = []
        for x in argv:
            if isinstance(x, int):
                comparisons.append(x)
            elif "operator" in x:
                if deal_with_new_node(x) == "undefined":
                    return "undefined"
                else:
                    comparisons.append(deal_with_new_node(x))
            elif "variable" in x:
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        return "undefined"
                    comparisons.append(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    return "undefined"
        if comparisons[0] == comparisons[1]:
            if comparisons [0] == "undefined" or comparisons[1] == "undefined":
                return "undefined"
            else:
                return 1
        return 0

        
    elif argument["operator"] == "member":
        comparisons = []
        for x in argv:
            if isinstance(x, int):
                comparisons.append(x)
            elif "operator" in x:
                if deal_with_new_node(x) == "undefined":
                    return "undefined"
                comparisons.append(deal_with_new_node(x))
            elif "variable" in x:
                if x["variable"] in variable_dict:
                    if x["variable"] == "undefined":
                        return "undefined"
                    comparisons.append(variable_dict[x["variable"]])
                else:
                    print "variable undefined"
                    print x["variable"]
                    return "undefined"
        if comparisons[0] in comparisons[1]:
            if not isinstance(comparisons[1],int):
                if comparisons [0] == "undefined" or comparisons[1] == "undefined":
                    return "undefined"
                else:
                    return 1
        return 0


"""===============================
INITIALIZE PARSING OF JSON FILE
==============================="""
#having 2 seperate parsing functions allows the program
#to ignore the first equals which is always assigning 
#a valiue to variable, rather than equivalence
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

        #if x is an integer then simply print the integer
        else:
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
#use imported json library to load json into dict input_data
input_data = json.load(json_file)

#inform user where output is going - just in case...
print '\nloaded \''+inwards+'\' as input'
print 'output to \''+outwards+'\' \n'
#for every member of the list with key 'statement-list' in the loaded dict
for x in input_data["statement-list"]:
    #parse the current member of the list
    parse_json(x)

#close opened files
f.close()
print '\nclosed \''+inwards+'\' - input file'
json_file.close()
print 'closed \''+outwards+'\' output file\n'
