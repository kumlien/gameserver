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
        
        try: 
            scoresLock.acquire()
            level = self.scores[new_score.level]
            logging.info('Before adding score: %s', str(list(map(lambda s: str(s.user_id) + ":" + str(s.score), level))))
            prev_score = None
            lowest_score = Score(0,0,0)
            rank = self.LIST_SIZE #Start with a rank just outside the top list
            for old_score in level:
                if old_score is None or old_score.score < new_score.score:
                    rank -= 1
                if old_score is not None and old_score.user_id == new_score.user_id:
                    prev_score = old_score
                if old_score is not None and lowest_score.score > old_score.score:
                    lowest_score = old_score

            logging.info('After checks, rank: %s, previous score %s and lowest score is %s', rank, prev_score, str(lowest_score.score))
            # if rank < 15: either replace the previous_score or the lowest_score
            if rank < 15:
                logging.info('Rank is lower than 15 (%s), either replace users previous score or replace the lowest score', rank)
                if prev_score is not None:
                    logging.info('User already has a score on the list (a score of %s), lets replace it', str(prev_score.score))
                    self.scores[new_score.level][:] = [new_score if x.user_id==new_score.user_id else x for x in level]
                else:
                    logging.info('User doesnt have a score on the list lets replace the lowest one (which has a score of %s)', str(lowest_score.score))
                    self.scores[new_score.level][:] = [new_score if x.user_id==lowest_score.user_id else x for x in level]
        finally:
            scoresLock.release()
        logging.info("Level %s is now %s", new_score.level, str(list(map(lambda s:s.score, self.scores[new_score.level]))))


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
