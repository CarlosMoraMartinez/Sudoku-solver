import sys
import copy as cp
import time
import os

import numpy as np
import pandas as pd

mat = np.array([[0,7,0,5,0,9,1,8,0],[4,9,8,0,2,0,0,3,5],[0,0,0,7,3,8,2,4,0],[0,4,7,9,8,0,0,6,0],[1,0,9,0,6,0,8,7,2],[0,2,0,0,1,0,0,9,4],[7,1,0,0,5,0,9,0,3],[0,8,5,2,9,0,6,0,7],[9,0,0,1,7,3,4,5,0]])
mat2 = np.array([[0,0,0,5,0,9,1,8,0],[4,9,0,0,2,0,0,3,5],[0,0,0,7,3,8,2,4,0],[0,4,7,9,8,0,0,6,0],[1,0,9,0,6,0,8,7,2],[0,2,0,0,1,0,0,9,4],[7,1,0,0,5,0,9,0,3],[0,8,5,2,9,0,6,0,7],[9,0,0,1,7,3,4,5,0]])
mat3 = np.array([[0,0,0,5,0,0,1,0,0],[4,9,0,0,2,0,0,0,5],[0,0,0,7,3,8,2,4,0],[0,4,7,9,8,0,0,6,0],[1,0,9,0,6,0,8,7,2],[0,2,0,0,1,0,0,9,4],[7,1,0,0,5,0,9,0,3],[0,8,5,2,9,0,6,0,7],[9,0,0,1,7,3,4,5,0]])
mat4 = np.array([[0,0,0,0,0,0,1,0,0],[4,9,0,0,0,0,0,0,5],[0,0,0,7,3,0,0,0,0],[0,4,7,9,8,0,0,6,0],[1,0,9,0,6,0,8,7,2],[0,2,0,0,1,0,0,9,4],[7,1,0,0,5,0,9,0,3],[0,8,5,2,9,0,6,0,7],[9,0,0,1,7,3,4,5,0]])

mat5 = np.array([[0,9,7,4,0,0,2,0,3],[0,3,0,0,0,0,6,9,0],[1,0,0,0,0,0,0,0,0],[0,0,0,1,0,9,0,0,4],[0,2,0,7,0,0,0,0,1],[0,0,0,0,0,0,7,0,0],[0,0,2,3,8,0,0,0,0],[3,0,0,6,0,1,9,7,0],[0,0,8,0,0,0,0,0,0]])
mat6 = np.array([[7,0,0,0,9,5,0,4,2],[0,0,2,1,8,0,7,0,0],[0,0,0,0,3,0,0,5,0],[6,0,0,0,0,0,0,0,8],[0,3,0,0,0,0,0,0,9],[4,9,0,0,7,0,0,1,0],[2,7,8,0,0,3,9,0,0],[1,0,6,7,0,0,0,0,0],[3,0,9,0,5,0,0,0,0]])
mat7 = np.array([[0,3,0,6,0,4,0,0,0],[0,0,9,7,0,0,5,0,0],[1,6,4,0,8,5,0,0,0],[0,4,6,0,0,2,0,0,0],[0,0,2,0,0,6,0,0,1],[8,0,0,0,0,7,0,0,0],[7,5,0,0,4,0,0,0,2],[0,0,8,0,0,0,0,5,0],[4,0,0,0,0,0,8,0,0]])

mat8 = np.array([[0,0,0,0,0,0,6,8,0],[0,0,0,0,7,3,0,0,9],[3,0,9,0,0,0,0,4,5],[4,9,0,0,0,0,0,0,0],[8,0,3,0,5,0,9,0,2],[0,0,0,0,0,0,0,3,6],[9,6,0,0,0,0,3,0,8],[7,0,0,6,8,0,0,0,0],[0,2,8,0,0,0,0,0,0]])
mat9 = np.array([[0,0,0,0,4,1,0,6,0],[0,0,0,0,0,0,0,3,0],[0,9,1,6,0,0,0,4,0],[6,0,4,9,3,0,0,0,0],[2,0,0,0,1,0,0,0,0],[0,0,0,0,0,5,0,0,0],[9,5,0,3,0,0,1,0,0],[0,8,6,0,2,0,0,9,0],[0,0,2,0,0,0,0,0,3]])

matbase = np.array([[],[],[],[],[],[],[],[],[]])


def solve(mat):
    solved = False
    stack = [(mat, 0, 0, 0)] #used for backtracking
    n_iter = 0
    t = time.time()
    while(not solved):
        n_iter+=1
        mat, x, y, newval = stack.pop() #take one option from stack
        if(newval != 0):
            mat[x, y] = newval #add chance value 
        mat = propagate(mat) #propagate constrains
        if(is_solved(mat)):
            solved = True
        else: 
            stack.extend(getAllOptions(mat)) # If can't keep propagating, add all options available to stack
    return (mat, n_iter, round(time.time() - t, 3))
def propagate(mat):
    propstack  = [(i, j) for i in range(9) for j in range(9) if mat[i, j] == 0]
    while(len(propstack)>0):
        x, y = propstack.pop()
        pos = getPossible(x, y, mat)
        if(len(pos) == 1):
            mat[x, y] = pos.pop()
            propstack.extend([n for n in getNeighbours(x, y, mat) if not n in propstack and mat[n]==0])
        else:
            pos = getUniquelyPossible(x, y, mat)
            if(len(pos) == 1):
                mat[x, y] = pos.pop()
                propstack.extend([n for n in getNeighbours(x, y, mat) if not n in propstack and mat[n]==0])
    return mat
def is_solved(mat):
    return np.all(mat != 0)     
def getNeighbours(x, y, mat, join = True):
    row = [(x, j) for j in range(0,9) if j != y]
    col = [(i, y) for i in range(0,9) if i != x]
    if(join):
        group = [(i, j) for i in range(0,9) for j in range(0,9) if (i//3 == x//3 and j//3 == y//3) and (i!=x and j!= y)] # no tuples repeated
        return row + col + group
    else:
        group = [(i, j) for i in range(0,9) for j in range(0,9) if (i//3 == x//3 and j//3 == y//3) and (i!=x or j!= y)]   # If groups are separated, each of them must contain all tuples
        return (row, col, group)
def getImpossible(x, y, mat):
    nei = getNeighbours(x, y, mat, True)
    impossible = set([int(mat[a, b]) for a, b in nei if mat[a, b] != 0])
    return impossible
def getPossible(x, y, mat):
    if(mat[x, y] != 0):
        return [int(mat[x, y])]
    else:
        return set([int(i) for i in range(1, 10)]) - getImpossible(x, y, mat)
def getAllOptions(mat):
    allpossible = set([i for i in range(1, 10)])
    options = [(cp.copy(mat), i, j, p) for i in range(9) for j in range(9) for p in list(allpossible - getImpossible(i, j, mat)) if mat[i, j] == 0]
    return options
def getUniquelyPossible(x, y, mat):
    this_possible = getPossible(x, y, mat)
    nei = getNeighbours(x, y, mat, False) #Neighbours separated by row, column or quadrant (group)
    uniquely_possible = [this_possible - set([pos for a, b in group for pos in getPossible(a, b, mat)  if mat[a, b] == 0]) for group in nei ] #get, for each neighbour group, which values cannot be taken by any other box
    uniquely_possible = [i for i in uniquely_possible if len(i) > 0]
    final_conj = set()
    for u in range(len(uniquely_possible)):
        if(u == 0):
            final_conj = final_conj.union(uniquely_possible[u])
        else:
            final_conj = final_conj.intersection(uniquely_possible[u])
    return final_conj        
def check(mat, ans = None):
    if(ans is None):
        badlist = []
        for i in range(9):
            for j in range(9):
                for a, b in getNeighbours(i, j, mat, True):
                    if(mat[i, j] == mat[a, b] or mat[i, j] == 0):
                        badlist.append(((i, j), (a, b)))
        return badlist 
    else:
        return np.where(mat != ans)[0].shape  
def testAll():
    i = 0
    for m in [mat, mat2, mat3, mat4, mat5, mat6, mat7, mat8]:
        s = solve(m)
        mist = len(check(s[0]))
        print(i, '\n', s, 'mistakes: ', mist, '\n', '*'*20, '\n')
        i +=1



def main():
    print('Testing sample matrixes...\n')
    testAll()
    print('Testing matrixes from file...\n')
    if(len(sys.argv)<2):
        fname = './sudoku.csv'
    else:
        fname = sys.argv[1]
    soduko = pd.read_csv(fname)
    for i in soduko.index:
        quiz = np.array([int(i) for i in soduko.quizzes[0]]).reshape(9, 9)
        answer = np.array([int(i) for i in soduko.solutions[0]]).reshape(9, 9)
        s = solve(quiz)
        mistakes = check(s[0], answer)
        print(i, ': mistakes ', mistakes)
if __name__== "__main__":
  main()

