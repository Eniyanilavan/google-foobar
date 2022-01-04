'''
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for the LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP -- and maybe sneak in a bit of sabotage while you're at it -- so you took the job gladly. 

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1
Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases -- 
Input:
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2

-- Java cases -- 
Input:
Solution.solution('4')
Output:
    2

Input:
Solution.solution('15')
Output:
    5
'''

def findMinSol(n, map={}):
    if map.get(n) != None:
        return map.get(n)
    if n == 3 or n == 5:
        return 2
    if n == 2:
        return 1
    if n == 1 :
        return 0
    if n == 0:
        return -1
    
    if n % 2 == 0:
        poss = findMinSol(n/2, map) + 1
        map[n] = poss
        print(map)
        return poss
    else:
        p1 = findMinSol(n/2+1, map)+1
        p2 = findMinSol(n/2-1, map)+2
        poss = min(p1, p2)+1
        map[n] = poss
        print(map)
        return poss

def solution(s):
    n = int(s)
    print(n)
    return findMinSol(n)

class StateSnapshot:

    n = 0
    stage = 0
    leftPossibilities = 0
    rightPossibilities = 0
    possibilities = 0

    def __init__(self, n):
        self.n = n
    
    def __repr__(self):
        return "<State n={} stage={} leftPossibilities={} rightPossibilities={} possibilities={}>".format(self.n, self.stage, self.leftPossibilities, self.rightPossibilities, self.possibilities)

def tempSolution(s, map = {}):
    n = int(s)
    stack = [StateSnapshot(n)]
    retuVal = 0

    while len(stack) != 0:
        state = stack.pop()
        num = state.n

        if map.get(str(num)) != None:
            retuVal = map.get(str(num))
            continue

        if num == 2:
            state.possibilities = 1
            retuVal = 1
            continue
        if num == 1 :
            state.possibilities = 0
            retuVal = 0
            continue
        if num == 0:
            state.possibilities = -1
            retuVal = -1
            continue
        
        elif num % 2 == 0:
            if state.stage == 0:
                stack.append(state)
                stack.append(StateSnapshot(num/2))
                state.stage = 1
            else:
                state.possibilities = retuVal + 1
                map[str(state.n)] = retuVal + 1
                retuVal = retuVal + 1
                pass
        else:
            if state.stage == 0:
                state.stage = 1
                stack.append(state)
                stack.append(StateSnapshot((num)+1))
            elif state.stage == 1:
                state.stage = 2
                stack.append(state)
                # print(retuVal)
                state.leftPossibilities = retuVal + 1
                stack.append(StateSnapshot((num)-1))
            else:
                state.rightPossibilities = retuVal + 1
                state.possibilities = min(state.leftPossibilities, state.rightPossibilities)
                retuVal = state.possibilities
                map[str(state.n)] = retuVal
                pass
    print(map) 
    return 1 if retuVal < 0 else retuVal
    
# print(tempSolution('1'))
# print("-----------------")
# print(tempSolution('2'))
# print("-----------------")
# print(tempSolution('3'))
# print("-----------------")
# print(tempSolution('4'))
# print("-----------------")
# print(tempSolution('5'))
# print("-----------------")
# print(tempSolution('6'))
# print("-----------------")
# print(tempSolution('7'))
# print("-----------------")
# print(tempSolution('8'))
# print("-----------------")
print(tempSolution('9'))
print("-----------------")
# print(tempSolution('10'))
# print("-----------------")
# print(tempSolution('11'))
# print("-----------------")
# print(tempSolution('12'))
# print("-----------------")
# print(tempSolution('13'))
# print("-----------------")
# print(tempSolution('14'))
# print("-----------------")
# print(tempSolution('15'))
# print("-----------------")
# print(tempSolution('90'))
# print("-----------------")
# print(tempSolution('309'))
print("-----------------")
print(tempSolution(int(''.join(['9' for _ in range(309)]))))#1336

# for i in range(0, 10):
#     print(i)
#     print(tempSolution(str(i)))
#     print("-----------------")