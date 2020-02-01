import json

class UsersController:
    def handleGet(self):
        print('Users controller called')
        user = {'name': 'Svante', 'age': 47}
        body = json.dumps(user)
        return 200, {'Content-type': 'Application/json'}, body