# coding: utf-8
import json 
from pprint import pprint
    
def output(t):
    counter = 0
    for x in t:
        if isinstance(x,frozenset):
            if counter != 0:
                print',',
            print '{',
            output(x)
            print'}',
            counter = counter+1
        elif isinstance(x,tuple):
            if counter != 0:
                print',',
            print'(',
            output(x)
            print')',
            counter = counter+1
        else:
            if counter != 0:
                print',',
            print(x),
            counter = counter+1
    
f = open('output.txt', 'w')
x = []
x.append(8)
x.append(frozenset([1,2,3,4,5,6,7,x[0]]))
x.append(frozenset([x[1],tuple([1,x[1]])]))
x.append(tuple([x[2],x[1]]))
x.append(frozenset([x[3]]).union(x[2]))
x.append(x[4].difference(frozenset([x[1]])))
x.append(x[4].intersection(frozenset([x[1]])))

for current in x:
    counter = 0
    if isinstance(current,frozenset):
        print ('{'),
        if counter != 0:
            print',',
        output(current)
        print '}',
        counter = counter+1
    elif isinstance(current,tuple):
        print '(',
        if counter != 0:
            print',',
        output(current)
        print ')',
        counter = counter+1
    else:
        print current,
        counter = counter+1
    print ';'

"""json_data=open('input.json')

data = json.load(json_data)
pprint(data)
json_data.close()"""

for current in x:
    counter = 0
    if isinstance(current,frozenset):
        f.write ('{'),
        if counter != 0:
            f.write(','),
        output(current)
        f.write ('}'),
        counter = counter+1
    elif isinstance(current,tuple):
        f.write ('('),
        if counter != 0:
           f.write (','),
        output(current)
        f.write (')'),
        counter = counter+1
    else:
        f.write(str(current)),
        counter = counter+1
    f.write(';')