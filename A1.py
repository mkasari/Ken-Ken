#!/usr/bin/env python
# coding: utf-8


#takes a row, column, and the cage information (coords, operators, target values)
#to return the information for the cage that the cell of (row, col) is associated with
def findCage(row, col, cageInfo):
    for i in range(len(cageInfo)):
        for j in cageInfo[i][0]:
            if j == (row, col):
                return cageInfo[i]

#finds the cage by calling findCage, takes an array of numbers to calculate,
#and calculates the cage based on the operator in the information array
def calculate(row, col, nums, cageInfo):
    opDict = {
        '+': np.add,
        '-': np.subtract,
        '*': np.multiply,
        '/': np.true_divide
    }

    info = findCage(row, col, cageInfo)

    val = int(info[1])
    op = info[2]

    tot = nums[0]
    alttot = nums[0]
    for n in nums[1:]:
            tot = opDict[op](tot, n)
    for n in nums[1:]:
        alttot = opDict[op](n,alttot)
    if tot == val or alttot == val:
        return True
    return False

#calls findCage and determines if each cell in the cage has been assigned a non-zero value
def cageIsFull(row, col, cageInfo, board):
    info = findCage(row, col, cageInfo)
    for i in info[0]:
        x = i[0]
        y = i[1]
        if board[x][y] != 0:
            return True
    return False

#calls cageIsFull and determines if the calculations are correct, and makes sure
def checkCage(board, cageInfo, row, col):
    if cageIsFull(row, col, cageInfo, board):
        nums = []
        info = findCage(row, col, cageInfo)
        for i in info[0]:
            x = i[0]
            y = i[1]
            nums.append(board[x][y])
        for j in nums:
            if j == 0:
                return True
        if calculate(row, col, nums, cageInfo):
            return True
        else:
            return False
    else:
        return True
    
#makes sure each values is non-zero and calls checkCage for each cell
def checkBoard(board, cageInfo):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]==0:
                return False
            if not checkCage(board, cageInfo, row, col):
                return False      
    return True

#assigns a value to each cell, checks the value and backtracks as needed to fix errors
def backtrack(board, cageInfo, n, arr):
    for i in range(n*n):
        row = i//n
        col = i%n
        if board[row][col] == 0:
            for value in range(1, n+1):
                if not value in board[row] and not value in board[:,col]:
                    board[row][col] = value
                    if checkBoard(board, cageInfo):
                        return True
                    else:
                        if backtrack(board, cageInfo, n, arr):
                            return True
                
            break
    arr.append(1)
    board[row][col] = 0
  




#
#add forward checking to backtracking function:




#creates a domain array to keep track of allowed values left in a row and column
#this induces forward checking by not allowing for numbers not within the domain to be set and checked
def fwdCheck(board, row, col):
    dom=[]
    for i in range(1, n+1):
        dom.append(i)
    for j in dom:
        if j in board[row] or j in board[:,col]:
            dom.remove(j)
            
    return dom

#same funtion as backtracking but uses the foward checking function
def backtrackPlus(board, cageInfo, n, arr):
    for i in range(n*n):
        row = i//n
        col = i%n
        if board[row][col] == 0:
            dom = fwdCheck(board, row, col)
            for value in dom:
                if not value in board[row] and not value in board[:,col]:
                    board[row][col] = value
                    if checkBoard(board, cageInfo):
                        return True
                    else:
                        if backtrackPlus(board, cageInfo, n, arr):
                            return True
            arr.append(1)    
            break
    
    board[row][col] = 0
    


    
    
#adding local search:




#appends values in the domain to an array
def createDom(n):
    dom = []
    for i in range(1,n+1):
        dom.append(i)
    return dom

#rotates the domain order for easily inputting unique values into rows and columns
def rotateDom(dom):
    return dom[1:] + dom[:1]

#creates a board with unique variables in the domain for each row and column
def createUboard(board):
    dom = createDom(n)
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                board[r][c] = dom[c]
        dom = rotateDom(dom)
    
    return board
#creates a board with random variables within the domain for each cell
def createRboard(board):
    dom = createDom(n)
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                board[r][c] = np.random.choice(dom)
    return board

#creates an array that counts the number of problems associated with each cell
#checks the row, the column, and the cage for a maximum of 3 issues per cell
def createProbs(board):
    probs = np.zeros((n,n)).astype(int)
    p=0
    for r in range(len(board)):
        for c in range(len(board)):
            t = board[r][c]
            board[r][c] = 0
            if t in board[r]:
                p += 1
            if t in board[:,c]:
                p += 1
            board[r][c] = t
            if not checkCage(board, cageInfo, r, c):
                p += 1
            probs[r][c] = p
            p=0
    return probs

#Creates a sum value of all the problems on the board for help with determining local maximums
def checkProbs(probs):
    s = 0
    for i in range(len(probs)):
        s += sum(probs[i])
    return s

#switches the values of two cells in the board
def swap(r1, c1, r2, c2, board):
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

# Local Search Function
# takes in the board to search
def localSearch(board, recursions):
    #probs is a board of the number of "problems" with each node (see createProbs function)
    probs = createProbs(board)
    #s is the number of probs of the current board (initialized to 100 to get started)
    s = 100
    #bb = best board, initalized to starting state
    bb = board
    #tries is the number of times we will try to solve the current board
    tries = 100
    #bp = best probs, initialized to the starting state probs board
    bp = probs
    #counter q
    countNode = 0
    q = 0
    while q <= tries:
        q+=1
        #loops through the values in the board
        for r in range(len(board)):
            for c in range(len(board)):
                for i in range(len(board)):
                    for j in range(len(board)):
                        countNode +=1
                        #swaps the MOST CONSTRAINED NODE (with max number of problems) with another node
                        #in the SAME ROW that has at least one problem
                        if r == i and (probs[r][c] == np.amax(probs) and probs[i][j]!= 0):
                            swap(r, c, i, j, board)
                            #sets probs to next probs board
                            probs = createProbs(board)
                            #t is the number of probs for the next board
                            t = checkProbs(probs)
                            #if the number of problems for the next board is less than the number
                            #of problems for the current board, set current = next and update best board and
                            #best prob board
                            if t < s:
                                s = t
                                bb = board
                                bp = createProbs(bb) 
                                #if there are no problems left, we've found the solution!
                                if s == 0:
                                    print(countNode)
                                    return countNode
                            #else, if the next number of problems is equal to the current number of problems,
                            #we are not getting any better, so we are at a LOCAL MAX so we should break and try again
                            elif t == s:
                                break
    #recursively call localSearch with a randomized board when you've reached a LOCAL MAX
    #to try solving it a different way, eventually you'll get there
    #we put in a recursion checker to make sure that we don't infinitely recur, to cover accidental infinite recursions
    if recursions < 1000:
        recursions += 1
        board3 = np.zeros((n,n)).astype(int)
        board3 = createRboard(board3)
        localSearch(board3, recursions)
    else: 
        print("NO SOLUTION FOUND")


if __name__=="__main__":
    #import libararies
    import numpy as np
    import sys
    
    #open file
    filename = sys.argv[1]
    file = open(filename)
    f = file.read().splitlines()

    #initialize lists and values
    n = int(f[0])
    mat = f[1:n+1]
    grid = []
    unique = []
    val = []
    op = []
    board = np.zeros((n,n)).astype(int)
    cageInfo = []
    arr = []

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            grid.append([mat[i][j], (i, j)])

    for q in range(len(grid)):
        if grid[q][0] not in unique:
            unique.append(grid[q][0])

    cages = np.empty((len(unique), 0)).tolist()
    rules = f[n+1:((n+1)+len(unique)+1)]

    for t in range(len(unique)):
        for q in range(len(grid)):
            if grid[q][0] == unique[t]:
                cages[t].append(grid[q][1])

    #creates an array of values and operators for each cage
    for z in range(len(rules)):
        val.append(rules[z][2:-1])
        op.append(rules[z][-1])

    #creates an complete array of coords for each cell in a cage, the target value and the operator
    for f in range(len(unique)):
        cageInfo.append([cages[f], val[f], op[f]])


    #solving the puzzle and counting nodes
    #backtracking solve:
    backtrack = backtrack(board, cageInfo, n, arr)
    if backtrack == True:
        print(board)
        print(len(arr))
    else:
        print("cannot solve with backtracking")

    #backtracking solve with forward checking:    
    board = np.zeros((n,n)).astype(int)
    arr = []
    backtrackPlus = backtrackPlus(board, cageInfo, n, arr)
    if backtrackPlus == True:
        print(len(arr))
    else:
        print('cannot solve with forward checking')
        
    #local search solve:
    #(please be patient, this one can be slow at times)
    board = np.zeros((n,n)).astype(int)
    board = createUboard(board)
    localSearch(board, 0)
