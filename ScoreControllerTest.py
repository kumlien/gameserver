import re
import uuid
import unittest
from src.controllers.ScoreController import Score
from src.controllers.ScoreController import ScoreController
from collections import defaultdict

class ScoreRepoTest(unittest.TestCase):

    def testGetScoreList(self):
        usersController = None # Yikes
        controller = ScoreController(usersController)
        scores = controller.handleGet(1)



if __name__ == '__main__':
    unittest.main()
