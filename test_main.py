import unittest
from main import timeCalculator
from main import getPos
from building import Building
# from building import Building


class mainTest(unittest.TestCase):
    b1 = Building("f.json")

    def test_something(self):
        # self.assertEqual(True, False)  # add assertion here
        self.assertFalse(len([]) != 0)


    def test_timeCalc(self):
        lst = [[0, 1, 1, [1]], [0, 1, 11, [3]], [-1, -1, 22, [19]], [-2, -1, 33, []], [0, 1, 45, [30]], [1, -1, 56, []]]

        print(timeCalculator(lst, 0))
        self.assertTrue(80 == timeCalculator(lst, 0))

    def test_getPos(self):
        lst = [[0, 1, 1, [1]], [0, 1, 11, [3]], [-1, -1, 22, [19]], [-2, -1, 33, []], [0, 1, 45, [30]], [1, -1, 56, []]]
        print(getPos(lst, 0, 50))
        self.assertTrue(-2 == getPos(lst, 0, 35)[0])






if __name__ == '__main__':
    unittest.main()
