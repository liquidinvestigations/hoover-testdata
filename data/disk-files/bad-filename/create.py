broken_name = 'modifi\udce9.txt'
with open(broken_name, 'w') as f:
    f.write('hello world\n')
    f.write('this is a broken filename with non-unicode entry\n')
