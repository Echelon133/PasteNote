import os
import uuid


def get_hash():
    return uuid.uuid4().hex[:10]


def create_file(filename, content):
    cwd = os.getcwd()
    filename = filename + '.txt'
    path = os.path.join(cwd, 'app/', 'downloads/', filename)
    with open(path, 'a') as f:
        f.write(content)
    return path

 
