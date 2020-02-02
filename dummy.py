import re
import uuid
import unittest

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


if __name__ == "__main__":
    unittest.main()