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
cycleCounter = 1

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
    def __init__(self, board, _domain=None, _domainLen=None, _assignment=None, _unassignedDomainLen=None):
        self.board = board
        self.boardIdx = _boardIdx
        self.domain = {}
        self.domainLen = {}
        self.unassignedDomainLen = {}
        self.MRVHeap = []
        self.assignment = {}

        if _domain is None:
            initialized = set()

            counter = 1
            for row in ROW:
                for col in COL:
                    key = f"{row}{col}"
                    value = self.board[key]
                    _domain, _domainLen = (set([value]), 1) if value != 0 else (set(range(1,10)), 9)
                    if _domainLen == 1:
                        self.assignment[key] = value
                    else:
                        self.unassignedDomainLen[key] = _domainLen

                    self.domain[key] = _domain
                    self.domainLen[key] = _domainLen

                    counter += 1

            for key in self.assignment.keys():
                self.forwardChecking(key)
        else:
            print("Using provided domain, domainLen, MRVHeap, assignment")
            # import pdb; pdb.set_trace()
            if None in [_domain, _domainLen, _assignment, _unassignedDomainLen]:
                raise ValueError("Either provide all or none of _domain, _domainLen, _MRVHeap, _assignment")
            self.domain              = _domain
            self.domainLen           = _domainLen
            self.assignment          = _assignment
            self.unassignedDomainLen = _unassignedDomainLen


    def assignNode(self, key, value):
        # if key == 'A3' and value == 8:
        #     import pdb; pdb.set_trace()
        newBoard, newDomain, newDomainLen, newAssignment, newUnassignedDomainLen = (self.board.copy(), self.domain.copy(), self.domainLen.copy(), self.assignment.copy(), self.unassignedDomainLen.copy())

        newBoard[key] = value
        newAssignment[key] = value
        newDomain[key] = set([value])
        newDomainLen[key] = 1
        newUnassignedDomainLen.pop(key, None)

        # import pdb; pdb.set_trace()
        newCspInstance = CSP(newBoard, newDomain, newDomainLen, newAssignment, newUnassignedDomainLen)
        

        forwardCheckResult = newCspInstance.forwardChecking(key)

        return newCspInstance if forwardCheckResult else False

    def forwardChecking(self, key):
        connectionHeap = self.getConnectionsHeap(key)



        while connectionHeap:
            _, _, connectionKey = heapq.heappop(connectionHeap)
            
            if self.board[key] in self.domain[connectionKey]:
                print(f"Forward Checking {key} -> {connectionKey} removing {self.board[key]}")
                print("Before", connectionKey, self.domain[connectionKey], self.domainLen[connectionKey])
                if connectionKey in self.unassignedDomainLen:
                    self.unassignedDomainLen[connectionKey] -= 1
                self.domainLen[connectionKey] -= 1
                if self.domainLen[connectionKey] == 0:
                    return False
                self.domain[connectionKey].remove(self.board[key])
                heapq.heappush(self.MRVHeap, (self.domainLen[connectionKey], self.boardIdx[connectionKey], connectionKey))

            else:
                pass

        return True

    def getConnectionsHeap(self, inputCell):
        connectionHeap = []

        inputRow = inputCell[0]
        inputCol = inputCell[1]

        # Get Row Connections
        cols = set(range(1,10))
        cols.remove(int(inputCol))

        for col in cols:
            heapq.heappush(connectionHeap, (len(self.domain[f"{inputRow}{col}"]), self.boardIdx[f"{inputRow}{col}"], f"{inputRow}{col}"))


        # Get Col Connections
        rows = set(chr(i) for i in range(65, 74))
        rows.remove(inputRow)

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
    



    

def backtracking2(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    csp = CSP(board)


    retval = backtracking_recursive(csp)

    return retval


class CSP2(object):
    def __init__(self, board, _domain=None, _domainLen=None):
        self.board = board
        self.domain = {}
        self.domainLen = {}
        self.boardIdx = _boardIdx
        
        if _domain is None:
            for row in ROW:
                for col in COL:
                    key = f"{row}{col}"
                    value = self.board[key]
                    self.domain[key], self.domainLen[key] = (set([value]), 1) if value != 0 else (set(range(1,10)), 9)
        else:
            print("Using provided domain, domainLen, assignment")
            if None in [_domain, _domainLen]:
                raise ValueError("Either provide all or none of _domain, _domainLen")
            self.domain    = _domain
            self.domainLen = _domainLen

    def forwardChecking(self, key):
        connectionHeap = self.getConnectionsHeap(key)
        updatedConnections = []

        while connectionHeap:
            _, _, connectionKey = heapq.heappop(connectionHeap)
            
            if self.board[key] in self.domain[connectionKey]:
                if self.domainLen[connectionKey] == 1:
                    return False
                
                updatedConnections.append(connectionKey)

            else:
                pass

        for connKey in updatedConnections:
            self.domainLen[connKey] -= 1
            self.domain[connKey].remove(self.board[key])
        return updatedConnections

    def getConnectionsHeap(self, inputCell):
        connectionHeap = []

        inputRow = inputCell[0]
        inputCol = inputCell[1]

        # Get Row Connections
        cols = set(range(1,10))
        cols.remove(int(inputCol))

        for col in cols:
            heapq.heappush(connectionHeap, (len(self.domain[f"{inputRow}{col}"]), self.boardIdx[f"{inputRow}{col}"], f"{inputRow}{col}"))


        # Get Col Connections
        rows = set(chr(i) for i in range(65, 74))
        rows.remove(inputRow)

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



def backtracking(board):
    csp = CSP2(board)
    retval = backtrack(csp)

def backtrack(assignment, csp):
    if checkComplete(assignment):
        return csp.board
    else:
        # Select unassigned variable with MRV
        var = MRV_select(csp)














def backtracking2(board):
    """Takes a board and returns solved board."""
    # TODO: implement this

    csp = CSP(board)


    retval = backtracking_recursive(csp)

    return retval

def backtracking_recursive(csp):
    # import pdb; pdb.set_trace()
    global cycleCounter
    print(f"\n\n\nCurrent Board {cycleCounter}: ")

    cycleCounter += 1
    # print(csp.board)
    if checkComplete(csp.assignment):
        return csp.board
    
    else:
        # while csp.unassignedDomainLen:
        print("Unassigned Domain Len", csp.unassignedDomainLen)

        minLen = key = None
        for _key, _domainLen in csp.domainLen.items():
            if _key not in csp.assignment:
                if minLen is None or _domainLen < minLen:
                    minLen = _domainLen
                    key = _key
                
        for value in csp.domain[key]:
            print("===================================")
            print(f"Selected Key: {key}")
            print("csp.domain of key", key, csp.domain[key])
            print(f"Selected value: {value}")
            print("Old", csp.domain)
            newCsp = csp.assignNode(key, value)
            print("New", newCsp.domain if newCsp is not False else "No new CSP")

            if newCsp is False:
                print("Backtracking from ", key, value)
                return False
            else:
                print("Calling Recursive")
                result = backtracking_recursive(newCsp)
                if result is not False:
                    return result
            # else:
            #     print("Skipping ", key, csp.domainLen[key], domainLen)
    return False

def checkComplete(assignment):
    if len(assignment) == 81:
        return True
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
        print(board_to_string(solved_board))
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")

    print("Finishing all boards in file.")