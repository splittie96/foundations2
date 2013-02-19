# coding: utf-8

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
            f.write(str(x))
            counter = counter+1

def write_out(to_write):
    if isinstance(to_write, int):
        f.write(str(to_write))
    elif isinstance(to_write, frozenset):
        f.write('{')
        output(to_write)
        f.write('}')
    elif isinstance(to_write,tuple):
        f.write('(')
        output(to_write)
        f.write (')')

x = []
x.append(8)
x.append(frozenset([1,2,3,4,5,6,7,x[0]]))
x.append(frozenset([x[1],tuple([1,x[1]])]))
x.append(tuple([x[2],x[1]]))
x.append(frozenset([x[3]]).union(x[2]))
x.append(x[4].difference(frozenset([x[1]])))
x.append(x[4].intersection(frozenset([x[1]])))

f = open('output.txt', 'w')
counter = 0
for current in x:
    f.write('x')
    f.write(str(counter))
    f.write(' = ')
    write_out(current)
    f.write(';\n')
    counter = counter + 1
    
f.close