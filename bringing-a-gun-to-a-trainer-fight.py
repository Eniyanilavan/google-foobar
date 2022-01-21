"""
Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).

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
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases -- 
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

#https://www.figma.com/file/yF6dbs4rl9g1h7ocJ9NnOQ/Untitled?node-id=0%3A1
https://www.desmos.com/calculator/onydjjnaxc
"""

from math import sqrt, atan, degrees

def distanceBetween(p1, p2):
    return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def slopeOfTwoPoints(p1, p2):
    if p2[0]-p1[0] == 0:
        return -1
    return float(p2[1]-p1[1])/float(p2[0]-p1[0])

def getAngle(p1, p2, slope):
    angle = degrees(atan(slope))

    #first quaderent
    if p2[0] - p1[0] > 0 and p2[1] - p1[1] >= 0:
        pass
    
    #sencond quaderent
    elif p2[0] - p1[0] < 0 and p2[1] - p1[1] >= 0:
        angle = 180 + angle

    #third quaderent
    elif p2[0] - p1[0] < 0 and p2[1] - p1[1]:
        angle = 180 + angle
    
    #forth quaderent
    elif p2[0] - p1[0] > 0 and p2[1] - p1[1] < 0:
        angle = 360 + angle
    
    if p2[0] == p1[0]:
        if p1[1] - p2[1] >= 0:
            angle = 90
        else:
            angle = 270
    
    return angle

def solution(dimensions, your_position, trainer_position, distance):

    reflectionsQueue = [[0, 0]]
    visitedSrcDir = {}
    visitedReflections = {}
    visitedDir = {}
    count = 0

    while len(reflectionsQueue) != 0:
        currRefl = reflectionsQueue.pop(0)

        visitedReflections["{},{}".format(currRefl[0], currRefl[1])] = 1
        
        srcInCurrRefX = (dimensions[0] - your_position[0]) if currRefl[0] % 2 != 0 else your_position[0]
        srcInCurrRefY = (dimensions[1] - your_position[1]) if currRefl[1] % 2 != 0 else your_position[1]
        srcInCurrRef = [(dimensions[0] * currRefl[0]) + srcInCurrRefX, (dimensions[1] * currRefl[1]) + srcInCurrRefY]

        targetInCurrRefX = (dimensions[0] - trainer_position[0]) if currRefl[0] % 2 != 0 else trainer_position[0]
        targetInCurrRefY = (dimensions[1] - trainer_position[1]) if currRefl[1] % 2 != 0 else trainer_position[1]
        targetInCurrRef = [(dimensions[0] * currRefl[0]) + targetInCurrRefX, (dimensions[1] * currRefl[1]) + targetInCurrRefY]

        currSlopeToTarget = slopeOfTwoPoints(your_position, targetInCurrRef)
        currSlopeToSrc = slopeOfTwoPoints(your_position, srcInCurrRef)

        currDir = getAngle(targetInCurrRef, your_position, currSlopeToTarget)#degrees(atan(currSlopeToTarget))
        currSrcDir = getAngle(srcInCurrRef, your_position, currSlopeToSrc)#degrees(atan(currSlopeToSrc))

        # |   is previously vesited dir    |  is src present in path     |                    if src present in path and currSrc is not in 0, 0          and      distance between src and currTarget greater than distance between src and currSrc           |  distance between src and target is less than given distance
        if visitedDir.get(currDir) != None or (currDir in visitedSrcDir) or (currSrcDir == currDir and (distanceBetween(your_position, srcInCurrRef) > 0 and distanceBetween(your_position, targetInCurrRef) > distanceBetween(your_position, srcInCurrRef))) or distanceBetween(your_position, targetInCurrRef) > distance:
            visitedSrcDir[currSrcDir] = 1
            continue

        visitedSrcDir[currSrcDir] = 1
        
        visitedDir[currDir] = 1

        count += 1

        # x+1, y
        if visitedReflections.get("{},{}".format(currRefl[0] + 1, currRefl[1])) == None:
            reflectionsQueue.append([currRefl[0] + 1, currRefl[1]])
        
        # x+1, y+1
        if visitedReflections.get("{},{}".format(currRefl[0] + 1, currRefl[1] + 1)) == None:
            reflectionsQueue.append([currRefl[0] + 1, currRefl[1] + 1])
        
        # x, y+1
        if visitedReflections.get("{},{}".format(currRefl[0], currRefl[1] + 1)) == None:
            reflectionsQueue.append([currRefl[0], currRefl[1] + 1])
        
        # x-1, y+1
        if visitedReflections.get("{},{}".format(currRefl[0] - 1, currRefl[1] + 1)) == None:
            reflectionsQueue.append([currRefl[0] - 1, currRefl[1] + 1])
        
        # x-1, y
        if visitedReflections.get("{},{}".format(currRefl[0] - 1, currRefl[1])) == None:
            reflectionsQueue.append([currRefl[0] - 1, currRefl[1]])
        
        # x-1, y-1
        if visitedReflections.get("{},{}".format(currRefl[0] - 1, currRefl[1] - 1)) == None:
            reflectionsQueue.append([currRefl[0] - 1, currRefl[1] - 1])

        # x, y-1
        if visitedReflections.get("{},{}".format(currRefl[0], currRefl[1] - 1)) == None:
            reflectionsQueue.append([currRefl[0], currRefl[1] - 1])
        
        # x+1, y-1
        if visitedReflections.get("{},{}".format(currRefl[0] + 1, currRefl[1] - 1)) == None:
            reflectionsQueue.append([currRefl[0] + 1, currRefl[1] - 1])
    
    return count

        

import time
start = time.time()
print(solution([3,2], [1,1], [2,1], 4))
print(solution([3,2], [2,1], [1,1], 4))
print(solution([300,275], [150,150], [185,100], 500))
print(solution([3,3], [1,1], [1,2], 4))
print(time.time()-start)
