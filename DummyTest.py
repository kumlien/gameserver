import re
import uuid
import unittest
import time
from src.controllers.UsersController import Session
from src.controllers.ScoreController import Score
from collections import defaultdict
from functools import reduce

def dummy():
    path = 'users/1'
    splitted = re.split(r'/', path)
    print(splitted)


class DummyTests(unittest.TestCase):
    
    def testSerializeDeSerializeUUID(self):
        id = uuid.uuid4()
        id_hex = id.hex
        id2 = uuid.UUID(id_hex)
        self.assertEqual(id, id2)

    def testSessionIsValidShouldReturnTrue(self):
        session = Session(1,1,time.time())
        self.assertTrue(session.isValid())

    def testEqualityOfListElements(self):
        scores = defaultdict(lambda: [None] * 15)
        score = Score(0,0,1)
        scores[0][0] = score
        scores[0].remove(score)

    def testListIndex(self):
        my_list = [None for n in range(4)]
        self.assertEqual(0, my_list.index(None))

    def testListReduce(self):
        my_list = [None for n in range(4)]
        my_list.append(Score(0,0,0))
        f = lambda a,b: a if (a is None) or (a > b) else b
        lowest = reduce(f, my_list)
        print(my_list.index(lowest))

if __name__ == "__main__":
    unittest.main()