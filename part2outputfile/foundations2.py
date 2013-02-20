# coding: utf-8
import json
from pprint import pprint

def parse_json(input_file, f):
	for x in input_data["statement-list"]:
		print (x["operator"])
		for y in x["arguments"]:
			print y

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

parse_json(input_data, f)
