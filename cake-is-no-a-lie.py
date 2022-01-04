'''The cake is not a lie!
======================

Commander Lambda has had an incredibly successful week: the first test of the LAMBCHOP doomsday device was completed AND Lambda set a new personal high score in Tetris. To celebrate, the Commander ordered cake for everyone -- even the lowliest of minions! But competition among minions is fierce, and if you don't cut exactly equal slices of cake for everyone you'll get in big trouble. 

The cake is round, and decorated with M&Ms in a circle around the edge. But while the rest of the cake is uniform, the M&Ms are not: there are multiple colors, and every minion must get exactly the same sequence of M&Ms. Commander Lambda hates waste and will not tolerate any leftovers, so you also want to make sure you can serve the entire cake.

To help you best cut the cake, you have turned the sequence of colors of the M&Ms on the cake into a string: each possible letter (between a and z) corresponds to a unique color, and the sequence of M&Ms is given clockwise (the decorations form a circle around the outer edge of the cake).

Write a function called solution(s) that, given a non-empty string less than 200 characters in length describing the sequence of M&Ms, returns the maximum number of equal parts that can be cut from the cake without leaving any leftovers.

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
solution.solution("abcabcabcabc")
Output:
    4

Input:
solution.solution("abccbaabccba")
Output:
    2

-- Java cases -- 
Input:
Solution.solution("abcabcabcabc")
Output:
    4

Input:
Solution.solution("abccbaabccba")
Output:
    2
'''

# def solutions(s):
#     lastIndex = len(s) - 1

#     lastChar = s[lastIndex]

#     subStrLen = lastIndex + 1

#     for endIndex in range(0, lastIndex + 1):
#         char = s[endIndex]
#         if endIndex > (lastIndex / 2):
#             break
#         if char == lastChar:
#             findex = endIndex
#             lindex = lastIndex
#             # print(findex, lindex)
#             while findex >= 0 and s[findex] == s[lindex]:
#                 findex -= 1
#                 lindex -= 1
#             if findex == -1:
#                 subStrLen = endIndex +1
#                 # break

#         endIndex += 1
    
#     # print(subStrLen)
#     if (lastIndex+1) % subStrLen != 0:
#         return 1
#     else:
#         return (lastIndex+1) / subStrLen

def solutions(s):
    leftIndex = 1
    preLeftIndex = 0
    length = len(s)

    if length == 0:
        return 0

    rightIndex = length - 1
    lastChar = s[rightIndex]
    subStrLen = length

    i = 0
    for char in s:
        if char != lastChar:
            break
        i += 1
    if i == length:
        return length

    while leftIndex < rightIndex:
        char = s[leftIndex]
        if char == lastChar:
            findex = leftIndex
            lindex = rightIndex
            print("pre", findex, lindex)
            if findex - preLeftIndex > subStrLen:
                break
            while findex >= preLeftIndex and s[findex] == s[lindex]:
                findex -= 1
                lindex -= 1
            if findex == preLeftIndex-1:
                preLeftIndex = leftIndex
                rightIndex = lindex
                if findex == -1:
                    subStrLen = leftIndex+1
                print("aft", leftIndex, rightIndex, preLeftIndex)
            # else:
            #     print("aft", leftIndex, rightIndex, preLeftIndex)
            #     breakrequest 
        leftIndex += 1
        
    print(leftIndex, rightIndex)
    if leftIndex <= rightIndex:
        return 1
    else:
        return length / subStrLen


print(solutions("abcabeabc"))
