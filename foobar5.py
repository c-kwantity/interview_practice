def solution(l):
    divisibleDict = getDivisibleList(l)
    print(divisibleDict)
    cnt = 0
    for startInd in xrange(len(l)):
        possSecondNum = divisibleDict[startInd]
        for secondIndex in possSecondNum:
            possTrips = divisibleDict[secondIndex]
            cnt += len(possTrips)
    return cnt

def getDivisibleList(numList):
    divisibleDict = {}
    for i in xrange(len(numList)):
        curNum = numList[i]
        divisibleList = []
        for j in xrange(i+1, len(numList)):
            testNum = numList[j]
            print("{0} -> {1} |  {2} -> {3} = {4}".format(i, curNum, j, testNum, testNum % curNum))
            if testNum % curNum == 0:
                divisibleList.append(j)
        divisibleDict[i] = divisibleList
    return divisibleDict

print(solution([1,1,1]))
print(solution([1,2,3,4,5,6]))