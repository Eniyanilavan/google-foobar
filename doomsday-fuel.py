'''
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

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases -- 
Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases -- 
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]

ref:
https://www.youtube.com/watch?v=qhnFHnLkrfA&list=PLANMHOrJaFxPMQCMYcYqwOCYlreFswAKP&index=9
'''

def decimalToFraction(n):
    tens = 10
    num1 = n*tens
    while num1 > 0 and num1 < 1000:
        num1 *= 10
        tens *= 10

    num2 = tens
    gcd = num1
    while gcd > 0 and True:
        if num2 > gcd:
            ans = num2 - gcd
        else:
            ans = gcd - num2
        if ans < 0.1:
            break
        num2 = gcd
        gcd = ans
    if gcd > 0:
        return [round(n*tens/gcd), round(tens/gcd)]
    else:
        return [0, 1]

def LeastCommonMultiple(n, m):
    lcm = 1
    while True:
        if lcm%n == 0 and lcm%m == 0:
            return lcm
        lcm += 1

def multiply(a, b, m, order, n):
    c = []
    for i in range(m):
        row = []
        for j in range(n):
            cij = 0
            for k in range(order):
                cij += a[i][k] * b[k][j]
            row.append(cij)
        c.append(row)
    
    return c


def inverse(m, order):

    I = [[float(1) if i == j else float(0) for j in range(order)] for i in range(order)]

    for i in range(0, order):
        for j in range(0, order):
            if i == j or m[j][i] == 0:
                continue
            else:
                ratio = float(m[i][i]) / m[j][i]
            for k in range(0, order):
                m[j][k] = (m[j][k] * ratio) - m[i][k]
                I[j][k] = (I[j][k] * ratio) - I[i][k]
            # print(m)
        
    for i in range(0, order):
        for j in range(0, order):
            I[i][j] = float(I[i][j]) / m[i][i]
        m[i][i] = float(m[i][i]) / m[i][i]
    
    return I



def solution(m):
    
    n = len(m)

    terminalStates = {}
    totalPossibilitiesInEachState = [0 for _ in range(n)]

    R = []
    Q = []

    #terminsalStates
    StateI = 0
    while StateI < n:
        s = m[StateI]
        posibilityI = 0
        while posibilityI < n:
            if s[posibilityI] != 0:
                break
            posibilityI += 1
        if posibilityI == n:
            terminalStates[StateI] = 1
        StateI += 1

    for i in range(n):
        totalPossibilitiesInEachState[i] = float(sum(m[i]))
    
    if terminalStates.get(0) != None:
        a = [1 if i==0 else 0 for i in range(len(terminalStates))]
        a.append(1)
        return a

    #rearrange for stable matrix (seperate R and Q)
    for rowI in range(0, n):
        if terminalStates.get(rowI) != None:
            continue
        row = m[rowI]
        index = 0
        Ri = []
        Qi = []
        while index < n:
            if terminalStates.get(index) != None:
                Ri.append(row[index] / totalPossibilitiesInEachState[rowI])
            else:
                Qi.append(row[index] / totalPossibilitiesInEachState[rowI])
            index += 1
        
        R.append(Ri)
        Q.append(Qi)
    
    # print(R)
    # print(Q)

    # I - Q
    for i in range(0, n - len(terminalStates)):
        for j in range(0, n - len(terminalStates)):
            if j == i:
                Q[i][j] = 1 - Q[i][j]
            else:
                Q[i][j] = 0 - Q[i][j]


    F = inverse(Q, n - len(terminalStates))

    # print(F)

    # print(len(F), len(R[0]))

    FR = multiply(F, R, len(F), len(R), len(R[0]))

    print(FR[0])
    
    fractions = []
    #decimal to simplest fraction
    for elem in FR[0]:
        fractions.append(decimalToFraction(elem))
    
    # print(fractions)
    
    LCM = 1
    for fraction in fractions:
        LCM = LeastCommonMultiple(LCM, fraction[1])
    
    output = []
    for fraction in fractions:
        rem = LCM/fraction[1]
        output.append(int(round(rem*fraction[0])))
    output.append(LCM)

    # print(output)
    return output

s = solution([[0, 0], [0, 0]])
print(s)


    




# print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
# m = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [4, 0, 0, 3, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# m.extend([[0 for _ in range(0, 10)] for _ in range(0, 4)])
# print(m)
# print(solution(m))



