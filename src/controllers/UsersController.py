import json

'''
Controller responsible or serving the 'users' resource. 
For now we bundle the controller with the repository
'''

class UsersRepo(object):
    users = {}

class User():
    def __init__(self, firstName, lastName, age):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age

    

class UsersController:

    def handleGet(self, id=None):
        print('Users controller called with id', id)
        body = ''
        code = 200
        if id is None:
            print('Return all users')
            body = json.dumps(UsersRepo.users.values)
        elif id in UsersRepo.users:
            user = UsersRepo.users[id]
            user = User('Svante', 'Kumlien', '47')
            body = json.dumps(user.__dict__)
        else:
            code = 404
            body = 'This is not the user you are looking for...'

        return code, {'Content-Type': 'Application/json; charset=UTF-8'}, body