#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


class CSP(object):
    def __init__(self, board):
        self.board = board
        self.domain = {key : [value] if value != 0 else list(range(1,10)) for key, value in board.items()}

        print(self.domain)

    def getRow(self, inputCell):
        inputRow = inputCell[0]
        inputCol = inputCell[1]

        cols = set(range(1,10)).remove(inputCol)

        row = {}
        rowKeys = set()
        for col in cols:
            row[f"{inputRow}{col}"] = self.domain[f"{inputRow}{col}"]
            rowKeys.add(f"{row}{inputCol}")

        return row, rowKeys

    def getCol(self, inputCell):
        inputRow = inputCell[0]
        inputCol = inputCell[1]

        rows = set(chr(i) for i in range(65, 74)).remove(inputRow)

        col = {}
        colKeys = set()
        for row in rows:
            col[f"{row}{inputCol}"] = self.domain[f"{row}{inputCol}"]
            colKeys.add(f"{row}{inputCol}")

        return col, colKeys

    def getSquare(self, inputCell):
        inputRow = inputCell[0]
        inputCol = inputCell[1]

        cols = []
        if int(inputCol) <= 3:
            cols = ['1', '2', '3']
        elif int(inputCol) >= 7:
            cols = ['7', '8', '9']
        else:
            cols = ['4', '5', '6']

        rows = []
        if ord(inputRow) - 64 <= 3:
            rows = ['A', 'B', 'C']
        elif ord(inputRow) - 64 >= 7:
            rows = ['G', 'H', 'I']
        else:
            rows = ['D', 'E', 'F']

        square = {}
        squarekeys = set()
        for row in rows:
            for col in cols:
                cell = f"{row}{col}"

                if cell == inputCell:
                    pass
                else:
                    square[cell] = self.domain[cell]
                    squarekeys.add(cell)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    print(board)

    # backtracking_recursive({}, board)
    solved_board = board
    return solved_board

def generateCSP(board):
    csp = {}
    csp.board
    return csp

def backtracking_recursive(assignment, board):

    return False

def checkComplete(assignment):
    return False

def minimumRemainingValueHeuristic(csp):
    return idx

def forwardChecking(csp):
    return False



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) < 9:
            print(sys.argv[1])
            print("Input string too short")
            exit()

        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")

    print("Finishing all boards in file.")