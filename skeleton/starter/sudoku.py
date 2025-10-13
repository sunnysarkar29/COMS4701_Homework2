#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import heapq

ROW = "ABCDEFGHI"
COL = "123456789"

_counter = 1
_boardIdx = {}
for _row in ROW:
    for _col in COL:
        key = f"{_row}{_col}"
        _boardIdx[key] = _counter
        _counter += 1




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
    def __init__(self, board, _domain=None, _MRVHeap=None):
        self.board = board
        self.boardIdx = _boardIdx

        if _domain is None:
            self.domain = {}
            self.domainLen = {}
            self.MRVHeap = []
            self.assignment = {}

            initialized = set()

            counter = 1
            for row in ROW:
                for col in COL:
                    key = f"{_row}{_col}"
                    value = self.board[key]
                    _domain, _domainLen = (set(value), 1) if value != 0 else (set(range(1,10)), 9)
                    if _domainLen == 1:
                        self.assignment[key] = value

                    self.domain[key] = _domain
                    self.domainLen[key] = _domainLen
                    self.forwardChecking(key)

                    counter += 1
        else:
            self.domain = _domain
            self.MRVHeap = _MRVHeap

        print(self.board)
        print(self.domain)
        print(self.connections)

    def forwardChecking(self, key):
        connectionHeap = self.getConnectionsHeap(key)

        while connectionHeap:
            _, _, connectionKey = heapq.heappop(connectionHeap)
            
            if self.board[key] in self.domain[connectionKey]:
                self.domainLen[connectionKey] -= 1
                if self.domainLen[connectionKey] == 0:
                    return False
                self.domain[connectionKey].remove(self.board[key])
                heapq.heappush(self.MRVHeap, (self.domainLen[connectionKey], self.boardIdx[connectionKey], connectionKey))

            else:
                pass

        return True

    # def getConnections(self, inputCell):
    #     connection = {}

    #     inputRow = inputCell[0]
    #     inputCol = inputCell[1]

    #     # Get Row Connections
    #     cols = set(range(1,10)).remove(inputCol)

    #     row = {}
    #     for col in cols:
    #         connection[f"{inputRow}{col}"] = self.domain[f"{inputRow}{col}"]

    #     # Get Col Connections
    #     rows = set(chr(i) for i in range(65, 74)).remove(inputRow)

    #     col = {}
    #     for row in rows:
    #         connection[f"{row}{inputCol}"] = self.domain[f"{row}{inputCol}"]

    #     # Get Square Connections
    #     cols = []
    #     if int(inputCol) <= 3:
    #         cols = ['1', '2', '3']
    #     elif int(inputCol) >= 7:
    #         cols = ['7', '8', '9']
    #     else:
    #         cols = ['4', '5', '6']

    #     rows = []
    #     if ord(inputRow) - 64 <= 3:
    #         rows = ['A', 'B', 'C']
    #     elif ord(inputRow) - 64 >= 7:
    #         rows = ['G', 'H', 'I']
    #     else:
    #         rows = ['D', 'E', 'F']

    #     square = {}
    #     squarekeys = set()
    #     for row in rows:
    #         for col in cols:
    #             cell = f"{row}{col}"

    #             if col == inputCol or row == inputRow:
    #                 """
    #                 A1 | A2 | A3
    #                 -------------
    #                 B1 | B2 | B3
    #                 -------------
    #                 C1 | C2 | C3

    #                 If Input Cell == B2
    #                     -> Row B Added from getRows
    #                     -> Col 2 Added from getCols

    #                 Avoid Duplicates don't add
    #                 """
    #                 pass
    #             else:
    #                 connection[cell] = self.domain[cell]

    #     return connection
        

    def getConnectionsHeap(self, inputCell):
        connectionHeap = []

        inputRow = inputCell[0]
        inputCol = inputCell[1]

        # Get Row Connections
        cols = set(range(1,10)).remove(inputCol)

        row = {}
        for col in cols:
            heapq.heappush(connectionHeap, (len(self.domain[f"{inputRow}{col}"]), self.boardIdx[f"{inputRow}{col}"], f"{inputRow}{col}"))


        # Get Col Connections
        rows = set(chr(i) for i in range(65, 74)).remove(inputRow)

        col = {}
        for row in rows:
            heapq.heappush(connectionHeap, (len(self.domain[f"{row}{inputCol}"]), self.boardIdx[f"{row}{inputCol}"], f"{row}{inputCol}"))

        # Get Square Connections
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

                if col == inputCol or row == inputRow:
                    """
                    A1 | A2 | A3
                    -------------
                    B1 | B2 | B3
                    -------------
                    C1 | C2 | C3

                    If Input Cell == B2
                        -> Row B Added from getRows
                        -> Col 2 Added from getCols

                    Avoid Duplicates don't add
                    """
                    pass
                else:
                    heapq.heappush(connectionHeap, (len(self.domain[cell]), self.boardIdx[cell], cell))

        return connectionHeap

    def getConnections(self, inputCell):
        connection = {}
        connectionHeap = []
        connectionKeys = set()

        inputRow = inputCell[0]
        inputCol = inputCell[1]

        # Get Row Connections
        cols = set(range(1,10)).remove(inputCol)

        row = {}
        for col in cols:
            connection[f"{inputRow}{col}"] = self.domain[f"{inputRow}{col}"]
            heapq.heappush(connectionHeap, (len(self.domain[f"{inputRow}{col}"]), self.boardIdx[f"{inputRow}{col}"], f"{inputRow}{col}"))
            connectionKeys.add(f"{inputRow}{col}")


        # Get Col Connections
        rows = set(chr(i) for i in range(65, 74)).remove(inputRow)

        col = {}
        for row in rows:
            connection[f"{row}{inputCol}"] = self.domain[f"{row}{inputCol}"]
            heapq.heappush(connectionHeap, (len(self.domain[f"{row}{inputCol}"]), self.boardIdx[f"{row}{inputCol}"], f"{row}{inputCol}"))
            connectionKeys.add(f"{row}{inputCol}")

        # Get Square Connections
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

                if col == inputCol or row == inputRow:
                    """
                    A1 | A2 | A3
                    -------------
                    B1 | B2 | B3
                    -------------
                    C1 | C2 | C3

                    If Input Cell == B2
                        -> Row B Added from getRows
                        -> Col 2 Added from getCols

                    Avoid Duplicates don't add
                    """
                    pass
                else:
                    connection[cell] = self.domain[cell]
                    heapq.heappush(connectionHeap, (len(self.domain[cell]), self.boardIdx[cell], cell))
                    connectionKeys.add(cell)

        return connection, connectionHeap, connectionKeys

    # def getRow(self, inputCell):
    #     inputRow = inputCell[0]
    #     inputCol = inputCell[1]

    #     cols = set(range(1,10)).remove(inputCol)

    #     row = {}
    #     rowHeap = []
    #     for col in cols:
    #         row[f"{inputRow}{col}"] = self.domain[f"{inputRow}{col}"]
    #         heapq.heappush(rowHeap, (len(self.domain[f"{inputRow}{col}"]), self.boardIdx[f"{inputRow}{col}"]))
    #         rowKeys.add(f"{row}{inputCol}")

    #     return row, rowKeys

    # def getCol(self, inputCell):
    #     inputRow = inputCell[0]
    #     inputCol = inputCell[1]

    #     rows = set(chr(i) for i in range(65, 74)).remove(inputRow)

    #     col = {}
    #     colKeys = set()
    #     for row in rows:
    #         col[f"{row}{inputCol}"] = self.domain[f"{row}{inputCol}"]
    #         colKeys.add(f"{row}{inputCol}")

    #     return col, colKeys

    # def getSquare(self, inputCell):
    #     inputRow = inputCell[0]
    #     inputCol = inputCell[1]

    #     cols = []
    #     if int(inputCol) <= 3:
    #         cols = ['1', '2', '3']
    #     elif int(inputCol) >= 7:
    #         cols = ['7', '8', '9']
    #     else:
    #         cols = ['4', '5', '6']

    #     rows = []
    #     if ord(inputRow) - 64 <= 3:
    #         rows = ['A', 'B', 'C']
    #     elif ord(inputRow) - 64 >= 7:
    #         rows = ['G', 'H', 'I']
    #     else:
    #         rows = ['D', 'E', 'F']

    #     square = {}
    #     squarekeys = set()
    #     for row in rows:
    #         for col in cols:
    #             cell = f"{row}{col}"

    #             if col == inputCol or row == inputRow:
    #                 """
    #                 A1 | A2 | A3
    #                 -------------
    #                 B1 | B2 | B3
    #                 -------------
    #                 C1 | C2 | C3

    #                 If Input Cell == B2
    #                     -> Row B Added from getRows
    #                     -> Col 2 Added from getCols

    #                 Avoid Duplicates don't add
    #                 """
    #                 pass
    #             else:
    #                 square[cell] = self.domain[cell]
    #                 squarekeys.add(cell)
    #     return square, squarekeys


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    csp_instance = CSP(board)
    print(board)

    backtracking_recursive({}, csp)
    solved_board = board
    return solved_board

def backtracking_recursive(assignment, board):

    return False

def checkComplete(assignment):
    if len(assignment) == 81:
        return True
    return False

def minimumRemainingValueHeuristic(csp):
    return idx




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