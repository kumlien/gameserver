import re
import uuid
import unittest
import time
from src.controllers.UsersController import Session
from src.controllers.ScoreController import Score
from src.controllers.ScoreController import ScoreRepo
from collections import defaultdict
from functools import reduce


class ScoreRepoTest(unittest.TestCase):

    def testAddFirstScore(self):
        repo = ScoreRepo()
        score1 = Score(1,1,1)
        level = repo.addScore(score1)
        correctScore = list(filter(lambda x: (x is not None) and (x.user_id == score1.user_id), level))
        self.assertEqual(1, len(correctScore))



if __name__ == '__main__':
    unittest.main()