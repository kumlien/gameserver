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
        self.assertTrue(level[0] == score1)
        nones = [score for score in level if score is None]
        self.assertEqual(14, len(nones))
    

    def testAddThreeScoresFromSameUser(self):
        repo = ScoreRepo()
        score1 = Score(1, 1, 1)
        score2 = Score(1, 1, 3)
        score3 = Score(1, 1, 2)
        repo.addScore(score1)
        repo.addScore(score2)
        level = repo.addScore(score3)

        self.assertTrue(level[0] == score3)
        nones = [score for score in level if score is None]
        self.assertEqual(14, len(nones))

    def testAddThreeScoresFromDifferentUsers(self):
        repo = ScoreRepo()
        score1 = Score(1,1,1)
        score2 = Score(2,1,1)
        score3 = Score(3,1,1)
        repo.addScore(score1)
        repo.addScore(score2)
        level = repo.addScore(score3)
        

        self.assertTrue(level[0] == score1)
        self.assertTrue(level[1] == score2)
        self.assertTrue(level[2] == score3)
        nones = [score for score in level if score is None]
        self.assertEqual(12, len(nones))

    def testAddScoreWithFullList(self):
        repo = ScoreRepo()
        level = None
        for i in range(15):
            level = repo.addScore(Score(i,1,i+1))
        
        score2 = Score(20, 1, 2)
        level = repo.addScore(score2)
        self.assertTrue(level[0] == score2)




if __name__ == '__main__':
    unittest.main()