import os

broken_name = 'modifi\udce9.txt'
broken_folder = 'folder_' + broken_name
broken_path = os.path.join(broken_folder, 'file_under_bad_folder_name')

os.makedirs(broken_folder, exist_ok=True)

with open(broken_name, 'w') as f:
    f.write('hello world\n')
    f.write('this is a broken filename with non-unicode entry\n')

with open(broken_path, 'w') as f:
    f.write('hello world 2\n')
    f.write('this is a filename inside a folder with a non-utf8 path\n')
