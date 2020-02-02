import json
import uuid
import time
import logging

'''
Controller responsible or serving the 'users' resource. 
For now we bundle the controller with the repository
'''
class SessionRepo(object):
    sessions = dict()
    
    #Add/update session for a user
    def putSession(self, session):
        logging.info('Saving session with id %s', session.id)
        self.sessions[session.id]=session

    def getSession(self, id):
        logging.info('Returning session with id %s', id)
        try:
            return self.sessions[id]
        except:
            return None

# A Session has an id, a user id and a timestamp when it was created.
class Session():
    max_age = 10 * 60

    def __init__(self, id, user_id, timestamp):
        self.id=id
        self.user_id = user_id
        self.timestamp = timestamp

    def isValid(self):
        return self.timestamp + self.max_age < time.time()


class UsersController:
    ID_FLOOR = 1000
    ID_CEILING = 9999
    sessionRepo = SessionRepo()

    def isValidSessionKey(self, sessionKey):
        logging.info('Validating sessionKey %s', sessionKey)
        session = self.sessionRepo.getSession(sessionKey)
        return session is not None and session.isValid()


    '''
    The GET request works like this:
        IF NO id is specified then we return the full users collection as a json struct.
        IF an id is specified we treat it as a LOGIN request for that (user-) id
        and upsert the session key record for that user. The id range is from 1000 -> 9999
    '''
    def handleGet(self, user_id=None):
        print('Users controller called with id', user_id)
        body = ''
        code = 200
        if user_id is None: # Return all users, no pagination for now
            body = json.dumps([ob.__dict__ for ob in self.sessionRepo.sessions.keys()])
        elif self.idWithinBounds(user_id): # User wants to login, give her a new session key
            session = Session(uuid.uuid4(), user_id, time.time())
            self.sessionRepo.putSession(session)
            body = json.dumps({'sessionKey':session.id.hex})
            print('Generated session key:', session.id)
        else: #Bad id, send 400
            code = 400
            body = json.dumps({'errorMessage':'id must be between ' + str(self.ID_FLOOR) + ' and ' + str(self.ID_CEILING)})
        
        return code, {'Content-Type': 'Application/json; charset=UTF-8'}, body

    #Return True if the user id is an int and in valid range
    def idWithinBounds(self, user_id):
        try:
            return self.ID_FLOOR <= int(user_id) <= self.ID_CEILING
        except:
            return False