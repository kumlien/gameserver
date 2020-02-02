import re
import uuid
import unittest
import time
from src.controllers.UsersController import Session

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

    def sessionIsValidShouldReturnTrue(self):
        session = Session(1,1,time.time())
        self.assertTrue(session.isValid())

if __name__ == "__main__":
    unittest.main()