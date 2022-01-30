"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
"""
import fractions

def solution(m):
    terminalStates = getTerminalStates(m)
    if len(terminalStates) == len(m): # all states are terminal and we start on 1
        zeroRes = [1] + [0 for i in xrange(len(terminalStates) - 1)]
        zeroRes.append(1)
        return zeroRes
    if len(terminalStates) == 0: # all states are terminal or transient
        raise Exception("Error. Does not end in a stable state")
    transientMatrix = getTransientMatrix(m, terminalStates)
    terminalMatrix = getTerminalMatrix(m, terminalStates)
    
    # absorbing markov chain
    # we need to calculate R (I - Q)^-1
    # (I - Q)^-1 is the fundamental matrix
    fundamentalMatrix = calcFundamentalMatrix(transientMatrix)
    probabilityFromState0 = []
    state0Transition = fundamentalMatrix[0]
    for stateIndex in xrange(len(terminalStates)):
        probability = (0,1)
        for transitionIndex in xrange(len(state0Transition)):
            probability = add(probability, multiply(state0Transition[transitionIndex], terminalMatrix[transitionIndex][stateIndex]))
        probabilityFromState0.append(probability)
    return tupleToResultFormat(probabilityFromState0)

def tupleToResultFormat(probabilityFromState0):
    # get gcd from tuples
    denominator = 1
    for probability in probabilityFromState0:
        denominator *= probability[1]
    result = [None] * len(probabilityFromState0)
    for i in xrange(len(probabilityFromState0)):
        probability = probabilityFromState0[i]
        commonMultiple = denominator / probability[1]
        result[i] = (commonMultiple * probability[0])
    result.append(denominator)
    gcd = result[0] # simplify to smallest common denominator
    for num in result:
        gcd = fractions.gcd(gcd, num)
    return [num / gcd for num in result]

def getTerminalStates(m):
    terminalStates = set()
    for row in xrange(len(m)):
        if sum(m[row]) == 0:
            terminalStates.add(row)
    return terminalStates

# this will generate a matrix of transient to transient states
def getTransientMatrix(m, terminalStates):
    transientMatrix = []
    for row in xrange(len(m)):
        if row in terminalStates: #skip terminal state
            continue
        denominator = sum(m[row])
        probabilityRow = []
        for col in xrange(len(m[row])):
            if col in terminalStates: #skip terminal state
                continue
            probabilityRow.append((m[row][col], denominator))
        transientMatrix.append(probabilityRow)
    return transientMatrix

# this will generate a matrix of transient to terminal state
def getTerminalMatrix(m, terminalStates):
    terminalMatrix = []
    for row in xrange(len(m)):
        denominator = sum(m[row])
        probabilityRow = []
        if row in terminalStates: # skip terminal state
            continue
        for col in xrange(len(m[row])):
            if col not in terminalStates: # need to end up in terminal
                continue
            probabilityRow.append((m[row][col], denominator))
        terminalMatrix.append(probabilityRow)
    return terminalMatrix

def calcFundamentalMatrix(transientMatrix):
    # I - Q, we minus the diagonal
    fundamentalMat = createIdentityMatrix(transientMatrix)
    for row in xrange(len(transientMatrix)):
        for col in xrange(len(transientMatrix[row])):
            fundamentalMat[row][col] = minus(fundamentalMat[row][col], transientMatrix[row][col])
    inverseMat = createIdentityMatrix(transientMatrix)
    # perform gaussian elimination
    # a1              a2           a3 
    # b1 - b1/a1 * a1 b2 - b1/a1 * a2 b3 - b1/a1 * a3
    # c1 - c1/a1 * a1 c2 - c1/a1 * a2 c3 - c1/a1 * a3
    # we remove lower triangle values
    # a1 a2 a3
    # 0  B2 B3
    # 0  0  C3
    for row in xrange(len(fundamentalMat)):
        for lowerTriangle in xrange(row + 1, len(fundamentalMat)):
            if fundamentalMat[row][row][0] == 0: # cannot divide by zero
                continue
            # we want to get the lower triangle to zero, so we compare that to the diagonal
            ratio = divide(fundamentalMat[lowerTriangle][row], fundamentalMat[row][row])
            for col in xrange(len(fundamentalMat[row])):
                cellValueMultiplyRatio = multiply(ratio, fundamentalMat[row][col])
                fundamentalMat[lowerTriangle][col] = minus(fundamentalMat[lowerTriangle][col], cellValueMultiplyRatio)
                # apply the same change to the inverse matrix
                invMatCellValueMultiplyRatio = multiply(ratio, inverseMat[row][col])
                inverseMat[lowerTriangle][col] = minus(inverseMat[lowerTriangle][col], invMatCellValueMultiplyRatio)
    # make diagonal all 1s
    for row in xrange(len(fundamentalMat)):
        diagVal = fundamentalMat[row][row]
        if diagVal[0] == 0: # cannot divide by zero
            continue
        for col in xrange(len(fundamentalMat[row])):
            fundamentalMat[row][col] = divide(fundamentalMat[row][col], diagVal)
            inverseMat[row][col] = divide(inverseMat[row][col], diagVal)
    # perform backsub in reverse row order
    # 1 a2 a3 | x1           x2 - z2 * a2 x3 - z3 * a3
    # 0  1 B3 | y1 - z1 * B3 y2 - z2 * B3 y3 - z3 * B3
    # 0  0  1 | z1           z2           z3
    for row in xrange(len(fundamentalMat) - 2, -1, -1):
        for upperTriangle in xrange(row + 1, len(fundamentalMat)):
            ratio = fundamentalMat[row][upperTriangle]
            for col in xrange(len(fundamentalMat[row])):
                cellValueMultiplyRatio = multiply(ratio, fundamentalMat[upperTriangle][col])
                fundamentalMat[row][col] = minus(fundamentalMat[row][col], cellValueMultiplyRatio)
                #apply the same to inverseMat
                invCellValueMultiplyRatio = multiply(ratio, inverseMat[upperTriangle][col])
                inverseMat[row][col] = minus(inverseMat[row][col], invCellValueMultiplyRatio)
    return inverseMat

def createIdentityMatrix(transientMatrix):
    inverseMat = []
    for row in xrange(len(transientMatrix)):
        newRow = [(1,1) if row == col else (0,1) for col in xrange(len(transientMatrix[row]))]
        inverseMat.append(newRow)
    return inverseMat

def multiply(fract1, fract2):
    if (fract1[1] == 0 or fract2[1] == 0):
        raise Exception("Denominator is zero.")
    numerator = fract1[0] * fract2[0]
    denominator = fract1[1] * fract2[1]
    commonDivisor = fractions.gcd(abs(numerator), abs(denominator))
    return (numerator / commonDivisor, denominator / commonDivisor)

def divide(fract1, fract2):
    return multiply(fract1, (fract2[1], fract2[0]))

def add(fract1, fract2):
    if (fract1[1] == 0 or fract2[1] == 0):
        raise Exception("Denominator is zero.")
    denominator = (fract1[1] * fract2[1])
    numerator = fract1[0] * fract2[1] + fract2[0] * fract1[1]
    gcd = fractions.gcd(abs(numerator), abs(denominator))
    res = (numerator / gcd, denominator / gcd)
    return res

def minus(fract1, fract2):
    return add(fract1, (fract2[0] * -1, fract2[1]))

print solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
print solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
print solution([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
print solution([[1,1,1],[0,0,0],[0,0,0]])
print solution([[0,1,0],[1,0,0],[0,0,0]])
print solution([[0,1,1],[0,0,0],[0,0,0]])
print solution([[0,0,0],[1,0,0],[1,0,0]])
