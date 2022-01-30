"""
You need to pass a message to the bunny workers, but to avoid detection, the code you agreed to use is... obscure, to say the least. The bunnies are given food on standard-issue plates that are stamped with the numbers 0-9 for easier sorting, and you need to combine sets of plates to create the numbers in the code. The signal that a number is part of the code is that it is divisible by 3. You can do smaller numbers like 15 and 45 easily, but bigger numbers like 144 and 414 are a little trickier. Write a program to help yourself quickly create large numbers for use in the code, given a limited number of plates to work with.

You have L, a list containing some digits (0 to 9). Write a function solution(L) which finds the largest number that can be made from some or all of these digits and is divisible by 3. If it is not possible to make such a number, return 0 as the solution. L will contain anywhere from 1 to 9 digits.  The same digit may appear multiple times in the list, but each element in the list may only be used once.
"""


def solution(l):
    # start by sorting the list so we always work with sorted array throughout
    l.sort(reverse=True)
    # a number is divisible by 3 if its sum is divisible by 3
    sumOfDigits = sum(l)
    remainder = sumOfDigits % 3
    if remainder == 0:
        return listToNum(l)
    else:
        # we construct a map of remainders to list of numbers.
        # because the main list was sorted, each remainder list is also sorted
        remainderDict = groupRemainders(l)
        remainderList = remainderDict[remainder]
        if len(remainderList) > 0:
            # we remove the number to make the sum divisible
            # note that the least number of items remove is best,
            # so we go with the single match
            remainderList.pop()
            return listToNum(mergeList(remainderDict.values()))
        else:
            altRemainder = 1 if remainder == 2 else 2
            altRemainderList = remainderDict[altRemainder]
            # if remainder is 1 and we remove 2 numbers with remainder 2,
            # we will make the number divisible
            # if remainder is 2 and we remove 2 numbers with remainder 1,
            # we will make the number divisible
            if len(altRemainderList) >= 2:
                altRemainderList.pop()
                altRemainderList.pop()
                return listToNum(mergeList(remainderDict.values()))
            else:
                return 0

def groupRemainders(sortedList):
    groupedRemainder = {0: [], 1: [], 2: []}
    for i in sortedList:
        groupedRemainder[i % 3].append(i)
    return groupedRemainder

def listToNum(sortedList):
    num = 0
    maxPower = len(sortedList) - 1
    for i in xrange(len(sortedList)):
        num += pow(10, maxPower - i) * sortedList[i]
    return num

# no need for optimization here, definitely less than 9 numbers
def mergeList(sortedListOfList):
    finalList = []
    for curList in sortedListOfList:
        finalList = finalList + curList
    finalList.sort(reverse=True)
    return finalList



print(solution([3,1,4,1,5,9]))