# coding: utf-8
import json
global variable_dict
variable_dict={}



def deal_with_new_node(argument):
    argv = argument["arguments"]
    if argument["operator"] == "set":
        newset = frozenset([])
        for x in argv:
            if isinstance(x, int):
                newset = newset.union([x])
            else:
                if "variable" in x:
                    newset = newset.union([variable_dict[x["variable"]]])
        return newset
    return 0

def parse_json(current):
	if current["operator"]=="equal":
            args = current["arguments"]
            var = args[0]["variable"]
            if isinstance(args[1], int):
                variable_dict[var] = args[1]
            else:
                variable_dict[var] = deal_with_new_node(args[1])
            






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

"""counter = 0
for current in x:
    f.write('x')
    f.write('%d' % counter)
    f.write(' = ')
    write_out(current)
    f.write(';\n')
    counter = counter + 1"""
f.close

print 'output to \'output.txt\' '
for x in input_data["statement-list"]:
    parse_json(x)

for key in sorted(variable_dict.iterkeys()):
    print "%s: %s" % (key, variable_dict[key])