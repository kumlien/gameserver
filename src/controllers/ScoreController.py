from src.controllers.UsersController import UsersController
import logging
import json
from collections import defaultdict
import threading
import logging
import uuid
from src.controllers import Utils

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
        self.scores = defaultdict(lambda: [None] * self.LIST_SIZE)

    # Add score IF it's in the top 15 AND the score is better than the users previous score
    def addScore(self, new_score):
        
        #first find out if new_score is among the top 15, if not bail out directly
        level = self.scores[new_score.level]
        isHighScore = any((s is None) or (s.score < new_score.score) for s in level)
        if not isHighScore:
            return level
        
        #Ok, we have a high-score. let's figure out which element to replace
        try:
            scoresLock.acquire()
            lowest_score = None
            
            #Replace:
            #1) users own score 2) None 3) lowest score entered
            score_replaced = False
            for i, current_score in enumerate(level):
                if current_score is not None and current_score.user_id == new_score.user_id: # User has a previous score
                    self.scores[new_score.level][:] = [new_score if x.user_id == new_score.user_id else x for x in level]
                    score_replaced = True
                    break
                if current_score is None: #There is a none in the list. This only works because real scores will always appear before None in the list...
                    level[i] = new_score
                    self.scores[new_score.level] = level
                    score_replaced = True
                    break
                elif lowest_score is None or lowest_score.score > current_score.score: # Set lowest score
                    lowest_score = current_score
            
            if not score_replaced:
                self.scores[new_score.level][:] = [new_score if x.user_id==lowest_score.user_id else x for x in level]
        finally:
            scoresLock.release()
        return self.scores[new_score.level]


class ScoreController:
    SESSION_KEY_PARAM = "sessionkey"
    score_repo = ScoreRepo()

    def __init__(self, usersController):
        self.users_controller = usersController

    def handlePost(self, level, score, query_params):
        try:
            score = json.loads(score)
            logging.info('handlePost for level %s, body %s and query %s', level, str(score), query_params)
            if int(score["score"]) < 1:
                return Utils.error(400, 'No scores lower than one please!')
            
            if int(level) < 1:
                return Utils.error(400, "No levels below one please!")

            if self.SESSION_KEY_PARAM not in query_params:
                return Utils.error(400, 'Missing query param: ' + self.SESSION_KEY_PARAM)
            
            sessionId = query_params[self.SESSION_KEY_PARAM][0]
            if not self.users_controller.isValidSessionKey(sessionId):
                return Utils.error(400,'Bad query param: ' + self.SESSION_KEY_PARAM)
            
            user_id = self.users_controller.getUserIdBySessionId(sessionId)
            score = Score(user_id, level, int(score['score']))
            self.score_repo.addScore(score)
            return Utils.ok()
        except Exception as error:
            logging.warn('Internal error when handling POST request', exc_info=True)
            return Utils.error(500, str(error))

    def handleGet(self, level):
        logging.info('Asked to return scores for level %s', level)
        return Utils.ok()
