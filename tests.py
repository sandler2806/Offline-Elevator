import unittest

from main import *


class mainTest(unittest.TestCase):

    def test_allocate(self):
        b1 = Building("f.json")
        calls= [[[0, 0, 0, []]] for q in range(len(b1.Elevators))]
        callsList=[['Elevator call', 15.74901825, 0, -6, 0, -1]]
        callsList1 = [['Elevator call', 24.346, 12, 80, 0, -1]]
        callsList2 = [['Elevator call', 53.1423, -3, 42, 0, -1]]
        json_List=['[[0, 0, 0, []]]', '[[0, 0, 0, []]]']
        c, ans = allocate(callsList, [[0], [1]], json_List, b1, calls)
        self.assertTrue([0] == ans)
        c, ans1 = allocate(callsList, [[1], [1]], json_List, b1, calls)
        self.assertTrue([1] == ans1)
        c, ans2 = allocate(callsList1, [[0], [1]], json_List, b1, calls)
        self.assertTrue([0] == ans2)
        c, ans3 = allocate(callsList2, [[0], [0]], json_List, b1, calls)
        self.assertTrue([0] == ans3)

    def test_timeCalc(self):
        lst = [[0, 0, 0], [0, 1, 1, [1]], [0, 1, 11, [3]], [-1, -1, 22, [19]], [-2, -1, 33, []], [0, 1, 45, [30]],
               [1, -1, 56, []]]
        lst2 = [[0, 0, 0, []], [-7, 1, 44, [31]], [-6, 1, 55, [47]], [-4, 4, 74, [63, 68, 68, 86]]]
        lst3 = [[0, 0, 0, []], [0, 1, 16, [16]], [-6, -1, 24, []], [-5, 1, 38, [31]], [-4, 2, 46, [30, 53]]]
        lst4 = [[0, 0, 0, []], [-2, 0, 187, [177]], [-1, -2, 195, [182]], [0, 1, 203, [166, 199]], [9, -1, 212, []]]

        self.assertTrue(80 == timeCalculator(lst, 0))
        self.assertTrue(81 == timeCalculator(lst2, 0))
        self.assertTrue(32 == timeCalculator(lst3, 0))
        self.assertTrue(39 == timeCalculator(lst4, 0))

    def test_getPos(self):
        b1 = Building("f.json")

        lst = [[0, 0, 0], [0, 1, 1, [1]], [0, 1, 11, [3]], [-1, -1, 22, [19]], [-2, -1, 33, []], [0, 1, 45, [30]],
               [1, -1, 56, []]]
        lst2 = [[0, 0, 0, []], [-7, 1, 44, [31]], [-6, 1, 55, [47]], [-4, 4, 74, [63, 68, 68, 86]]]
        lst3 = [[0, 0, 0, []], [0, 1, 16, [16]], [-6, -1, 24, []], [-5, 1, 38, [31]], [-4, 2, 46, [30, 53]]]
        lst4 = [[0, 0, 0, []], [-2, 0, 187, [177]], [-1, -2, 195, [182]], [0, 1, 203, [166, 199]], [9, -1, 212, []]]

        self.assertTrue(-2 == getPos(lst, 0, 35, b1)[0])
        self.assertTrue(-5 == getPos(lst2, 0, 61, b1)[0])
        self.assertTrue(-4 == getPos(lst3, 0, 44, b1)[0])
        self.assertTrue(0 == getPos(lst4, 0, 205, b1)[0])

    def test_insert(self):
        b1 = Building("f.json")

        initial = [[0, 0, 0]]
        insert_call(initial, 0, 0, -1, 1, b1)
        insert_call(initial, 0, 0, -1, 3, b1)
        insert_call(initial, 0, -1, -2, 19, b1)
        insert_call(initial, 0, 0, 1, 30, b1)
        insert_call(initial, 0, 2, 1, 70, b1)

    def test_baseX(self):
        self.assertTrue(decToBaseX(0, 4, 5) == [0, 0, 0, 0, 0])
        self.assertTrue(decToBaseX(11, 3, 5) == [0, 0, 1, 0, 2])
        self.assertTrue(decToBaseX(20, 2, 5) == [1, 0, 1, 0, 0])
        self.assertTrue(decToBaseX(30, 4, 5) == [0, 0, 1, 3, 2])


if _name_ == '_main_':
    unittest.main()