import unittest
from io import StringIO
from contextlib import redirect_stdout
from libs import asyncmongo as nosql
from unittest import IsolatedAsyncioTestCase

class TestAsync(IsolatedAsyncioTestCase):
    """
    Testing  for async functions
    """
    def setUp(self) -> None:
        self.mongouri = "mongodb://localhost"
    async def test_db(self):
        db = nosql.AsyncMongo(uri=self.mongouri, db="test")
        with redirect_stdout(StringIO()) as sout:
            await db.ping_server()
            val = sout.getvalue().rstrip('\n')
            exp = "Pinged your deployment. You successfully connected to MongoDB!"
            self.assertEqual(exp, val)



class Test(unittest.TestCase):
    '''
    testing for sync func
    '''
    def setUp(self) -> None:
        self.mongouri = "mongodb://localhost"

    def test_dummy(self):
        db = nosql.AsyncMongo(uri=self.mongouri, db="test")
        val = db.foo()
        self.assertEqual(self.mongouri, val)
