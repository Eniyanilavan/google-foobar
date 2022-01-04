'''
Running with Bunnies
====================

You and the bunny workers need to get out of this collapsing death trap of a space station -- and fast! Unfortunately, some of the bunnies have been weakened by their long work shifts and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close. 

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave -- you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest worker IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by worker ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the solution is [1, 2].

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
Solution.solution({{0, 1, 1, 1, 1}, {1, 0, 1, 1, 1}, {1, 1, 0, 1, 1}, {1, 1, 1, 0, 1}, {1, 1, 1, 1, 0}}, 3)
Output:
    [0, 1]

Input:
Solution.solution({{0, 2, 2, 2, -1}, {9, 0, 2, 2, -1}, {9, 3, 0, 2, -1}, {9, 3, 2, 0, -1}, {9, 3, 2, 2, 0}}, 1)
Output:
    [1, 2]

-- Python cases -- 
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
[0, 1, 1, 1, 1], 
[1, 0, 1, 1, 1], 
[1, 1, 0, 1, 1], 
[1, 1, 1, 0, 1], 
[1, 1, 1, 1, 0]]
Output:
    [0, 1]
'''
class HeapNode:
    timeTaken = 0
    numBunniesTill = 0
    numNodesTill = 0
    left = None
    right = None
    index = 0
    path = set()

    def __init__(self, index, value, numBunniesTill, numNodesTill, path):
        self.timeTaken = value
        self.numBunniesTill = numBunniesTill
        self.numNodesTill = numNodesTill
        self.index = index
        self.path = path

    def swap(self, node):
        temp = self.timeTaken
        self.timeTaken = node.timeTaken
        node.timeTaken = temp

        temp = self.numBunniesTill
        self.numBunniesTill = node.numBunniesTill
        node.numBunniesTill = temp

        temp = self.numNodesTill
        self.numNodesTill = node.numNodesTill
        node.numNodesTill = temp

        temp = self.index
        self.index = node.index
        node.index = temp

        temp = self.path
        self.path = node.path
        node.path = temp

    def __repr__(self):
        return "<HeapNode timeTaken={} numBunniesTill={} index={} \n\tleft={} \n\tright={}>".format(self.timeTaken, self.numBunniesTill, self.index, self.left, self.right)

class Heap:
    head = None
    length = 0

    def heapify(self, root):
        if root == None:
            return
        self.heapify(root.left)
        self.heapify(root.right)

        if root.left != None and root.numBunniesTill <= root.left.numBunniesTill:
            if root.numBunniesTill < root.left.numBunniesTill or (root.numBunniesTill == root.left.numBunniesTill and root.timeTaken > root.left.timeTaken):
                root.swap(root.left)

        if root.right != None and root.numBunniesTill <= root.right.numBunniesTill:
            if root.numBunniesTill < root.right.numBunniesTill or (root.numBunniesTill == root.right.numBunniesTill and root.timeTaken > root.right.timeTaken):
                root.swap(root.right)

    def push(self, node):
        self.length += 1
        if self.head == None:
            self.head = node
        else:
            queue = [self.head]
            while len(queue) != 0:
                currNode = queue.pop(0)
                if currNode.left == None:
                    currNode.left = node
                    break
                elif currNode.right == None:
                    currNode.right = node
                    break
                else:
                    queue.append(currNode.left)
                    queue.append(currNode.right)
            self.heapify(self.head)          

    def pop(self):
        if self.length == 0:
            return None
        self.length -= 1
        val = self.head

        if self.length == 0:
            self.head = None
            return val

        queue = [self.head]
        lastNodeParent = self.head
        while len(queue) != 0:
            currNode = queue.pop(0)
            if currNode.left == None:
                temp = lastNodeParent.right
                lastNodeParent.right = None
                temp.left = self.head.left
                temp.right = self.head.right
                self.head = temp
                break
            elif currNode.right == None:
                temp = currNode.left 
                currNode.left = None
                temp.left = self.head.left
                temp.right = self.head.right
                self.head = temp
                break
            else:
                queue.append(currNode.left)
                queue.append(currNode.right)
            lastNodeParent = currNode
        
        self.heapify(self.head)
        
        val.left = None
        val.right = None
        return val
    
    def __repr__(self):
        return "{}".format(self.head)
    
def checkNegativeCycle(times, n):

    shortestPath = [ 1000 for _ in range(n)]
    shortestPath[0] = 0
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if times[j][k] + shortestPath[j] < shortestPath[k]:
                    shortestPath[k] = times[j][k] + shortestPath[j]

    for j in range(n):
            for k in range(n):
                if times[j][k] + shortestPath[j] < shortestPath[k]:
                    return True

    return False


def solution(times, time_limit):
    N = 0
    n = len(times)

    visited = {}

    if checkNegativeCycle(times, n):
        return [i for i in range(0, n-2)]
    
    result = HeapNode(0, 0, 0, 0, set())
    priorityQueue = Heap()
    priorityQueue.push(HeapNode(0, 0, 0, 0, set()))

    minDis = [9999 for _ in range(n)]

    for i in range(n):
        minRowVal = 999
        for j in range(n):
            if i == j:
                continue
            timeRow = times[i][j]
            if timeRow < minRowVal:
                minRowVal = timeRow
        minDis[i] = minRowVal
    
    i = 0

    while priorityQueue.length != 0:
        currElem = priorityQueue.pop()
        remTime = time_limit - currElem.timeTaken
        cache = visited.get("{},{}".format(currElem.index, currElem.timeTaken))
        if not (cache != None and cache.numBunniesTill >= currElem.numBunniesTill):
            for neighbour in range(n):
                if currElem.index == neighbour:
                    continue
                if currElem.numNodesTill <= n*n and (currElem.timeTaken + times[currElem.index][neighbour] <= time_limit or minDis[neighbour] < 0) or (neighbour == n-1 and remTime >= times[currElem.index][neighbour]):
                    path = currElem.path.copy()
                    numBunniesTill = 0
                    if neighbour != 0 and neighbour != n-1 and neighbour not in path:
                        numBunniesTill = 1
                    if neighbour != 0 and neighbour != n-1:
                        path.add(neighbour)
                    nextNode = HeapNode(neighbour, (times[currElem.index][neighbour] + currElem.timeTaken), currElem.numBunniesTill + numBunniesTill, currElem.numNodesTill + 1, path)
                    priorityQueue.push(nextNode)
        
            visited["{},{}".format(currElem.index, currElem.timeTaken)] = currElem
            
        if currElem.index == n-1 and currElem.timeTaken <= time_limit:
            if (currElem.numBunniesTill > result.numBunniesTill):
                result = currElem
            elif currElem.numBunniesTill == result.numBunniesTill and sum(currElem.path) < sum(result.path):
                result = currElem
            if currElem.numBunniesTill == n-2:
                break
        
    return [] if result == None else [i-1 for i in result.path]