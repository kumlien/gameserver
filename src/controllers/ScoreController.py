from src.controllers.UsersController import UsersController
import logging
import json
from collections import defaultdict
import threading
import logging

# A score for a specific user for a specific level and of course a score
class Score(object):
    def __init__(self, user_id, level, score):
        self.user_id = user_id
        self.level = level
        self.score = score

scoresLock = threading.Lock()
class ScoreRepo(object):
    LIST_SIZE = 15

    def __init__(self):
        # Map with level as key and list of scores as value
        self.scores = defaultdict(lambda: [Score(0,0,0)] * self.LIST_SIZE)

    # Add score IF it's in the top 15 AND the score is better than the users previous score
    def addScore(self, new_score):
        try: 
            scoresLock.acquire()
            level = self.scores[new_score.level]
            prev_score = None
            lowest_score = None
            rank = self.LIST_SIZE
            for score in level:
                if score.score < new_score.score:
                    rank -= 1
                if score.user_id == new_score.user_id:
                    prev_score = score

            logging.info('After checks, rank: %s and previous score %s', rank, prev_score)
            # if rank < 15: either replace the previous_score or the lowest_score
                


        finally:
            scoresLock.release()


class ScoreController:
    SESSION_KEY_PARAM = "sessionkey"
    score_repo = ScoreRepo()

    def __init__(self, usersController):
        self.users_controller = usersController

    def handlePost(self, level, score, query_params):
        score = json.loads(score)
        logging.info('handlePost for level %s, body %s and query %s', level, str(score), query_params)
        if self.SESSION_KEY_PARAM not in query_params:
            return 400, {"Content-Type": "application/json"}, json.dumps({'errorMessage': 'Missing query param: ' + self.SESSION_KEY_PARAM})
        
        sessionId = query_params[self.SESSION_KEY_PARAM][0]
        if not self.users_controller.isValidSessionKey(sessionId):
            return 400,{"Content-Type": "application/json"},json.dumps({'errorMessage': 'Bad query param: ' + self.SESSION_KEY_PARAM})
        
        user_id = self.users_controller.getUserIdBySessionId(sessionId)
        score = Score(user_id, level, int(score['score']))
        if self.score_repo.addScore(score):
            return 201, {"Content-Type": "application/json"}, json.dumps(score)
        return 200, {"Content-Type": "application/json"}, None

    def handleGet(self, level):
        logging.info('Asked to return scores for level %s', level)
        return 200, {"Content-Type": "application/json"}, None
