import re
import uuid
import unittest
import time
from collections import defaultdict
from functools import reduce

# content of test_sample.py
class TestClass:
    def func(self, x):
        return x + 1


    def test_answer(self):
        assert self.func(3) == 4
