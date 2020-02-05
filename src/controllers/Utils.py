import json

def error(code, message='N/A'):
    if message:
        return code, {"Content-Type": "application/json"}, json.dumps({'errorMessage': message})
    return code, {"Content-Type": "application/html"}, json.dumps({'errorMessage': message})

def ok(message=None):
    return 200, {"Content-Type": "application/json"}, json.dumps(message)

def created(id, resource):
    return 201, {"Location": id, "Content-Type": "application/json"}, json.dumps(resource)