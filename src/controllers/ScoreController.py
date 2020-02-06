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

# Move this repo to it's own file
class ScoreRepo(object):
    LIST_SIZE = 15

    def __init__(self):
        # Map with level as key and list of scores as value
        self.scores = defaultdict(lambda: [None] * self.LIST_SIZE)

        # Map with level as key and a lock as value
        self.locks = defaultdict(lambda: threading.Lock())

    # Get the current list of scores for the specified level
    # Order by score desc and then by user_id asc
    def getLevelSorted(self, level):
        logging.debug("Raw scores for level %s: %s", level, self.scores[level])
        scores = [score for score in self.scores[level] if score is not None]
        scores.sort(key = lambda score: score.user_id, reverse=False)
        scores.sort(key = lambda score: score.score, reverse=True)
        logging.debug("Scores for level %s: %s", level, scores)
        return scores

    # Add score IF it's in the top 15 AND the score is better than the users previous score
    # Return the list of scores for the level of new_score
    def addScore(self, new_score):
        
        #first find out if new_score is among the top 15, if not bail out directly
        level = self.scores[new_score.level]
        isHighScore = any((s is None) or (s.score < new_score.score) for s in level)
        if not isHighScore:
            return level
        
        # Ok, we have a high-score. let's figure out which element to replace
        with self.locks[new_score.level]:
            lowest_score = None
            
            # Replace either
            # 1) users own score 2) Any None value 3) lowest score in the list
            score_replaced = False
            for i, current_score in enumerate(level):
                if current_score is not None and current_score.user_id == new_score.user_id: # User has a previous score
                    self.scores[new_score.level][:] = [new_score if x is not None and x.user_id == new_score.user_id else x for x in level]
                    score_replaced = True
                    break
                if current_score is None: #There is a none in the list. This only works because real scores will always appear before None in the list...
                    level[i] = new_score
                    self.scores[new_score.level] = level
                    score_replaced = True
                    break
                elif lowest_score is None or lowest_score.score > current_score.score: # Save lowest score so far
                    lowest_score = current_score
            
            if not score_replaced: # Score not replaced yet, replace lowest score
                self.scores[new_score.level][:] = [new_score if x.user_id==lowest_score.user_id else x for x in level]

        logging.debug("ScoreRepo: level %s after adding score: %s", new_score.level, self.scores[new_score.level])
        return self.scores[new_score.level]


class ScoreController:
    SESSION_KEY_PARAM = "sessionkey"

    def __init__(self, usersController, scoreRepo=ScoreRepo()):
        self.users_controller = usersController
        self.score_repo = scoreRepo

    def handlePost(self, level, score, query_params):
        try:
            sessionId = query_params[self.SESSION_KEY_PARAM][0]
            if not self.users_controller.isValidSessionKey(sessionId):
                return Utils.error(403)

            score = json.loads(score)
            logging.info('handlePost for level %s, body %s and query %s', level, str(score), query_params)
            
            if int(score["score"]) < 1:
                return Utils.error(400, 'No scores lower than one please!')
            if int(score["score"]) > 2147483647:
                return Utils.error(400, 'No scores higher than 2147483647 please!')
            
            if int(level) < 1:
                return Utils.error(400, "No levels below one please!")
            if int(level) > 2147483647:
                return Utils.error(400, "No levels below one please!")

            if self.SESSION_KEY_PARAM not in query_params:
                return Utils.error(400, 'Missing query param: ' + self.SESSION_KEY_PARAM)
            
            user_id = self.users_controller.getUserIdBySessionId(sessionId)
            score = Score(user_id, level, int(score['score']))
            logging.info("Adding score %s", score.__dict__)
            self.score_repo.addScore(score)
            logging.info("Level is %s after adding score", self.score_repo.getLevelSorted(level))
            return Utils.ok()
        except Exception as error:
            logging.warn('Internal error when handling POST request', exc_info=True)
            return Utils.error(500, str(error))

    # GET the (15 top) scores for the specified level
    def handleGet(self, level):
        logging.info('Asked to return scores for level %s', level)
        if int(level) < 1:
            return Utils.error(400, "No levels below one please!")
        if int(level) > 2147483647:
            return Utils.error(400, "No levels below one please!")
        l = list()
        for score in self.score_repo.getLevelSorted(level):
            l.append({'user': score.user_id, 'score': score.score})
        
        return Utils.ok(l)
