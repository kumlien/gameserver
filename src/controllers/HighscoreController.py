from src.controllers.UsersController import UsersController
import logging
import json

# A score for a specific user for a specific level and of course a score
class Score(object):
    def __init__(self, user_id, level, score):
        self.user_id = user_id
        self.level = level
        self.score = score


class HighscoreController:
    SESSION_KEY_PARAM = "sessionkey"
    def __init__(self, usersController):
        self.users_controller = usersController

    def handlePost(self, level, score, query_params):
        logging.info('handlePost for level %s, body %s and query %s', level, str(score), query_params)
        if self.SESSION_KEY_PARAM not in query_params:
            return 400, {"Content-Type": "application/json"}, json.dumps({'errorMessage': 'Missing query param: ' + self.SESSION_KEY_PARAM})
        
        if not self.users_controller.isValidSessionKey(query_params[self.SESSION_KEY_PARAM][0]):
            return 400,{"Content-Type": "application/json"},json.dumps({'errorMessage': 'Bad query param: ' + self.SESSION_KEY_PARAM})
        return 200, {"Content-Type": "application/json"}, None