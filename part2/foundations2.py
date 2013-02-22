#CHARACTER ENCODING INFO
#ALLOWS USE OF '#' WITHOUT ANGRY ERROR MESSAGES
# coding: utf-8

#IMPORT JSON LIBRARY
import json
#GLOBAL DICTIONARY OF ALL PARSED VARIABLES
variable_dict={}

"""===============================
RECURSIVE PARSING OF OPERATORS
==============================="""
def deal_with_new_node(argument):
    #takes in the list of arguments ascociated with the argument key
    argv = argument["arguments"]
    #checks
    if argument["operator"] == "set":
        newset = set([])
        for x in argv:
            if isinstance(x, int):
                newset.add(x)
            elif "operator" in x:
		newset.add(deal_with_new_node(x))
            elif "variable" in x:
		newset.add(variable_dict[x["variable"]])
            new_frozenset = frozenset(newset)
        return new_frozenset
        
    elif argument["operator"] == "tuple":
	tuple_contents = []
	for x in argv:
            if isinstance(x, int):
		tuple_contents.append(x)
            elif "operator" in x:
		tuple_contents.append(deal_with_new_node(x))
            elif "variable" in x:
		tuple_contents.append(variable_dict[x["variable"]])
	new_tuple = tuple(tuple_contents)
	return new_tuple
    
    elif argument["operator"] == "equal":
	comparisons = []
        counter = 0
	for x in argv:
            if isinstance(x, int):
		comparisons.append(x)
            elif "operator" in x:
		comparisons.append(deal_with_new_node(x))
            elif "variable" in x:
		comparisons.append(variable_dict[x["variable"]])
            counter = counter + 1
        if comparisons[0] == comparisons[1]:
            if not isinstance(comparisons[1],int):
                return 1
        
    elif argument["operator"] == "member":
	comparisons = []
        counter = 0
	for x in argv:
            if isinstance(x, int):
		comparisons.append(x)
            elif "operator" in x:
		comparisons.append(deal_with_new_node(x))
            elif "variable" in x:
		comparisons.append(variable_dict[x["variable"]])
            counter = counter + 1
        if comparisons[0] in comparisons[1]:
            return 1
    
    return 0


"""===============================
INITIALIZE PARSING OF JSON FILE
==============================="""
def parse_json(current):
    if current["operator"]=="equal":
        argv = current["arguments"]
        var = argv[0]["variable"]
        if isinstance(argv[1], int):
            variable_dict[var] = argv[1]
        else:
            variable_dict[var] = deal_with_new_node(argv[1])
    f.write (var + " = ")			
    write_out(variable_dict[var])
    f.write(';\n')


"""====================================
METHOD TO CARRY OUT RECURSIVE PRINTING
===================================="""
def output(out):
    counter = 0
    for x in out:
        if isinstance(x,frozenset):
            if counter != 0:
                f.write(',')
            f.write('{')
            output(x)
            f.write('}')
            counter = counter+1
        elif isinstance(x,tuple):
            if counter != 0:
                f.write(',')
            f.write('(')
            output(x)
            f.write (')')
            counter = counter+1
        else:
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
    #if set, print relevant brackets then reccurse on contained set
    elif isinstance(to_write, frozenset):
        f.write('{')
        output(to_write)
        f.write('}')
    #if tuple, print relevant brackets then recurse on contained tuple
    elif isinstance(to_write,tuple):
        f.write('(')
        output(to_write)
        f.write (')')


"""===============================
MAIN PROGRAM RUNS HERE
==============================="""
#open output.txt for writing evaluated expressions
f = open('output.txt', 'w')
#open json file for reading
json_file = open('simple-input.json', 'r')
#use imported json library to load json into dict input_data
input_data = json.load(json_file)

#inform user where output is going - just in case...
print 'output to \'output.txt\' '
#for every member of the list with key 'statement-list' in the loaded dict
for x in input_data["statement-list"]:
    #parse the current member of the list
    parse_json(x)

#close opened files
f.close()
json_file.close()