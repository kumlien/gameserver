from src.controllers.UsersController import UsersController
import logging

# A score for a specific user for a specific level and of course a score
class Score(object):
    def __init__(self, user_id, level, score):
        self.user_id = user_id
        self.level = level
        self.score = score


class HighscoreController:
    def __init__(self, usersController):
        self.users_controller = usersController

    def handlePost(self, level, score, query_params):
        logging.info('handlePost for level %s, body %s and query %s', level, str(score), query_params)
        return 200, {"Content-Type": "application/json"}, None