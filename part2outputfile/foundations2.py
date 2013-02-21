# coding: utf-8
import json
variable_dict={}

def deal_with_new_node(argument):
    argv = argument["arguments"]
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

def write_out(to_write):
    if isinstance(to_write, int):
        f.write('%d' % to_write)
    elif isinstance(to_write, frozenset):
        f.write('{')
        output(to_write)
        f.write('}')
    elif isinstance(to_write,tuple):
        f.write('(')
        output(to_write)
        f.write (')')

x=[]
f = open('output.txt', 'w')
json_file = open('input.json', 'r')
input_data = json.load(json_file)

print 'output to \'output.txt\' '
for x in input_data["statement-list"]:
    parse_json(x)

f.close