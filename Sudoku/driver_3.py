import numpy as np
import pandas as pd
import sys
import queue
import time
import copy


input_string = sys.argv[1]


def sudoku_solver(input_string):

    # Define CSP class
    class csp_class:
        def __init__(self, Domains, Constraint, X, board):
            self.D = Domains       # Domains
            self.C = Constraint    # Constraints
            self.sudoku = board    # Board with values assigned
            self.X = X             #variables

    # Dictionary
    board = {}

    # Variables list
    Variables = []

    # boxes list
    box_list = []
    box_list.append(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
    box_list.append(['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'])
    box_list.append(['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'])
    box_list.append(['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'])
    box_list.append(['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'])
    box_list.append(['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'])
    box_list.append(['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'])
    box_list.append(['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'])
    box_list.append(['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9'])

    # create dictionary and initial domains
    count = 0
    Domain = {}
    for j in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:

            k= j+str(i)
            Variables.append(k)
            if int(input_string[count]) == 0:
                Domain[k] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                board[k] = 0
            else:
                Domain[k] = [int(input_string[count])]
                board[k] = int(input_string[count])

            count = count + 1

    # Constraint check function
    def constraint(x,y):
        return (x!=y)

    # Box finding function
    def box(x):

        if x[1] == str(1) or x[1] == str(2) or x[1] == str(3):
            a = [1, 4, 7]
        if x[1] == str(4) or x[1] == str(5) or x[1] == str(6):
            a = [2, 5, 8]
        if x[1] == str(7) or x[1] == str(8) or x[1] == str(9):
            a = [3, 6, 9]

        if x[0] == 'A' or x[0] == 'B' or x[0] == 'C':
            b = [1, 2, 3]
        if x[0] == 'D' or x[0] == 'E' or x[0] == 'F':
            b = [4, 5, 6]
        if x[0] == 'G' or x[0] == 'H' or x[0] == 'I':
            b = [7, 8, 9]

        c = set(a).intersection(b)

        return c

    # Check if x,y are in same box
    def checkbox(x,y):

        b1 = box(x)
        b2 = box(y)

        return (b1 == b2)

    # Generate constraints
    Constraints = {}
    def genconstraints():
        for i in range(0,len(Variables)):
            item = []
            x = Variables[i]
            for j in range(0, len(Variables)):
                if i == j:
                    continue
                y = Variables[j]
                if x != y:
                    r1,c1 = x[0],x[1]
                    r2,c2 = y[0],y[1]
                    if (r1 == r2) or (c1==c2) or checkbox(x,y):
                        item.append(y)
            Constraints[x] = item

    genconstraints()

    # Revise function

    def revise(csp, x, y):

        revised = False

        for xi in csp.D[x]:
            if not any([constraint(xi, yi) for yi in csp.D[y]]):
                csp.D[x].remove(xi)
                revised = True
        return revised

    # AC-3 Algorithm
    def AC3(csp):

        # queue of arcs:
        q = [(i, j) for i in csp.D for j in csp.C[i]]

        while q:
            x,y = q.pop()
            a = set(q)

            if len(csp.D[x]) == 0:
                return False

            if revise(csp, x, y):
                for xi in csp.C[x]:
                    if y != xi:
                        item = (xi,x)
                        if not item in a:
                            q.append(item)

        return True

    # completeness check:
    def complete_check(csp):

        success = True

        for key,val in csp.sudoku.items():
            if val == 0:
                success = False
                break

        return  success

    # heursitic - MRV
    def MRV2(csp):

        prev_length = 10
        for var in csp.X:
            if len(csp.D[var]) < prev_length and csp.sudoku[var] == 0:
                min_var = var
                prev_length = len(csp.D[var])
        return min_var


    # Consistency check:
    def consistent2(csp, var, val):
        valid = True

        for x in csp.C[var]:
            if csp.sudoku[x] == val:
                valid = False

        return valid

    # Forward checking algorithm:
    def forward_check(csp):

        # AC3
        #AC3(csp)

        # Downsizing the domains:
        for x in csp.X:
            if(len(csp.D[x]) == 1):
                for c in csp.C[x]:
                    if csp.D[x][0] in csp.D[c]:
                        csp.D[c].remove(csp.D[x][0])

                if csp.sudoku[x] == 0:
                    csp.sudoku[x] = csp.D[x][0]

        return


    # Back Tracking Algorithm
    def backtrack(csp):

        state = copy.deepcopy(csp)
        forward_check(state)
        if all([(len(state.D[k]) == 1 and state.sudoku[k] != 0)for k in state.X]):
            return state

        if not any([len(state.D[k]) == 0 for k in state.X]): 
            var = MRV2(state)  # MRV
            for value in state.D[var]: 
                child_state = copy.deepcopy(state)
                child_state.D[var] = [value]
                result = backtrack(child_state)
                if result is not None:
                    return result
        return None

    # Actual calls to solver
    def solve(csp):

        AC3(csp)
        result = backtrack(csp)
        output_string = ''
        for var in csp.X:
            output_string += str(result.sudoku[var])
        fp = open("output.txt",'w')
        #print(output_string)
        fp.write(output_string)
        fp.close()

    return solve(csp_class(Domain,Constraints,Variables,board))

sudoku_solver(input_string)
