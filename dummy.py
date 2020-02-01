import re

def dummy():
    path = 'users/1'
    splitted = re.split(r'/', path)
    print(splitted)

if __name__ == "__main__":
    dummy()