from util import *

class Square:
    def __init__(self):
        self.occupied = False
        self.type = EMPTY_SQUARE
        self.eval = {d: 0 for d in DIRECTIONS}
        self.square_id = [0] * 8
        self.neigh_occupied_squares = {d: False for d in DIRECTIONS}

    def not_connected(self):
        return not any(self.neigh_occupied_squares.values())

    def total_score(self):
        return sum(self.eval.values())

    def abs_total_score(self):
        sum1 = 0
        values = self.eval.values()
        for i in values:
            sum1 += abs(i)
        return sum1
