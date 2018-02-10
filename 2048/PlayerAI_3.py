from random import randint
from BaseAI_3 import BaseAI
import time
import math

class PlayerAI(BaseAI):

    max_depth = 3
    start = 0
    from_time = 0

    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        best = self.decision(grid)
        return best if moves else None


    def decision (self,grid):
        self.start = time.clock()
        prev_best = None
        depth = 3
        newGrid = grid.clone()
        while (time.clock() - self.start) < 0.2 and self.from_time == 0:
            bestMove, score = self.Maximize(newGrid, depth, -100000000, 100000000)
            if(self.from_time == 0):
                prev_best = bestMove
            depth = depth + 1
            newGrid = grid.clone()

        if self.from_time == 1:
            self.from_time = 0
            bestMove = prev_best

        return bestMove

    def Maximize(self, grid, depth, alpha, beta):

        if depth == 0:
            return None, self.Eval(grid)

        MaxUtility = -10000000000
        MaxMove = None
        valid_moves = grid.getAvailableMoves()

        if time.clock() - self.start > 0.195:
            valid_moves = []
            self.from_time = 1


        if len(valid_moves) == 0:
            MaxUtility = alpha


        for dir in valid_moves:

            newGrid = grid.clone()
            if newGrid.move(dir) is True:

                move, utility = self.Minimize(newGrid, depth-1, alpha, beta)

                if utility > MaxUtility:
                    MaxUtility = utility
                    MaxMove = dir

                if MaxUtility >= beta:
                    break

                if MaxUtility > alpha:
                    alpha = MaxUtility

        return MaxMove, MaxUtility

    def Minimize(self, grid, depth, alpha, beta):

        if depth == 0:
            return None, self.Eval(grid)

        MinMove = -1
        MinUtility = 100000000

        cells = grid.getAvailableCells()

        if (time.clock() - self.start) > 0.195:
            cells = []
            self.from_time = 1

        if len(cells) == 0:
            MinUtility = beta

        flag = 0

        for i in range(0, 2):
            for j in range(0, len(cells)):
                newGrid = grid.clone()
                newGrid.insertTile(cells[j], pow(2, i + 1))
                move, utility = self.Maximize(newGrid, depth-1, alpha, beta)

                if utility < MinUtility:
                    MinMove = move
                    MinUtility = utility

                if  MinUtility <= alpha:
                    flag = 1
                    break

                if beta < MinUtility:
                    MinUtility = beta
            if flag == 1:
                break

        return MinMove, MinUtility


    def Eval(self, grid):

        return self.grid_weights(grid)-self.penalty_scattered(grid)


 


    def grid_weights(self,grid):


        """
        W.append([0.135759, 0.121925, 0.10828, 0.099937])
        W.append([0.0997992, 0.0888405, 0.076711, 0.0161889])
        W.append([0.06065, 0.0562, 0.037116, 0.161889])
        W.append([0.0125498, 0.0099, 0.0057, 0.0033])


        W.append([6, 5, 4, 3])
        W.append([5, 4, 3, 2])
        W.append([4, 3, 2, 1])
        W.append([3, 2, 1, 0])

        """
        """
        W.append([6, 5, 4, 3])
        W.append([5, 4, 3, 2])
        W.append([4, 3, 2, 1])
        W.append([3, 2, 1, 0])

        """
        W = [[6, 5, 4, 1],
                    [5, 4, 1, 0],
                    [4, 1, 0, -1],
                    [1, 0, -1, -2]];


        wscore = 0
        for i in range(0, 4):
            for j in range(0, 4):
                wscore += W[i][j] * grid.map[i][j]

        return wscore


    def penalty_scattered(self, grid):


        penalty = 0
        for i in range(0, 4):
            for j in range(0, 4):
                num_neighbour = 0
                # Penalty for scattered cells
                pen_cell = 0
                if i - 1 > 0:
                    pen_cell += math.fabs(grid.map[i][j] - grid.map[i-1][j])


                if i + 1  < 4:
                    pen_cell += math.fabs(grid.map[i][j] - grid.map[i + 1][j])

                if j-1 > 0:
                    pen_cell += math.fabs(grid.map[i][j] - grid.map[i][j-1])
                    num_neighbour += 1

                if j+1 < 4:
                    pen_cell += math.fabs(grid.map[i][j] - grid.map[i][j+1])
                    num_neighbour += 1

                penalty += pen_cell/num_neighbour

        return penalty



