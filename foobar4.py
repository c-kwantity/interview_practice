"""
Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions. 

You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). 

Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.

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
solution.solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])
Output:
    7

Input:
solution.solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
Output:
    11

-- Java cases -- 
Input:
Solution.solution({{0, 1, 1, 0}, {0, 0, 0, 1}, {1, 1, 0, 0}, {1, 1, 1, 0}})
Output:
    7

Input:
Solution.solution({{0, 0, 0, 0, 0, 0}, {1, 1, 1, 1, 1, 0}, {0, 0, 0, 0, 0, 0}, {0, 1, 1, 1, 1, 1}, {0, 1, 1, 1, 1, 1}, {0, 0, 0, 0, 0, 0}})
Output:
    11
"""

from collections import deque

# def solution(map):
#     h = len(map)
#     w = len(map[0])
#     minLen = h + w - 1
#     startVertex = Vertex(0, 0, 1, 1)
#     # only cardinal directions allowed
#     moves = [(-1,0), (1,0), (0,-1), (0,1)]

#     # we save the distances we have encountered
#     # even wall distances should be saved
#     distArray = [[None] * w for i in xrange(h)]
#     # keep track of which vertices have alr been visited before
#     seenVertex = [[False] * w for i in xrange(h)]

#     # we use bfs to determine shortest length
#     queue = deque([startVertex])
#     seenVertex[startVertex.row][startVertex.col] = True
#     distArray[startVertex.row][startVertex.col] = startVertex

#     while len(queue) > 0:
#         curVertex = queue.popleft()
#         if curVertex.row == (h - 1) and curVertex.col == (w - 1):
#             break
#         # vertices and their weights are added to dist and seen
#         # walls should be added too
#         for move in moves:
#             row = curVertex.row + move[0]
#             col = curVertex.col + move[1]
#             if row < 0 or row >= h or col < 0 or col >= w:
#                 continue
#             if map[row][col] == 1: # is a wall
#                 if seenVertex[row][col]:
#                     nextVertex = distArray[row][col]
#                     if nextVertex.passedWallCnt <= 0:
#                         nextVertex.passWallCnt += 1
#                         nextVertex.wallDistance = curVertex.distance + 1
#                 else:
#                     if curVertex.passedWallCnt <= 0:
#                         nextVertex = Vertex(row, col, None, curVertex.distance + 1, curVertex.passedWallCnt + 1)
#                         seenVertex[nextVertex.row][curVertex.col] = True
#                         distArray[nextVertex.row][nextVertex.col] = nextVertex
#                         queue.append(nextVertex)
#             else:
#                 if seenVertex[row][col]:
#                     nextVertex = distArray[row][col]
#                     if curVertex.distance is None: # reached here by going through a wall, there is no wall-less path
#                         nextVertex.wallDistance = min(nextVertex.wallDistance, curVertex.wallDistance + 1)
#                     else:
#                         nextVertex.distance = min(nextVertex.distance, curVertex.distance + 1) if nextVertex.distance is not None else curVertex.distance + 1
#                         nextVertex.wallDistance = min(nextVertex.wallDistance, curVertex.distance + 1)
#                 else:
#                     if curVertex.distance is None: # reached here by going through a wall, there is no wall-less path
#                         nextVertex = Vertex(row, col, None, curVertex.wallDistance + 1, curVertex.passedWallCnt)
#                     else:
#                         nextVertex = Vertex(row, col, curVertex.distance + 1, curVertex.wallDistance + 1, curVertex.passedWallCnt)
#                     seenVertex[nextVertex.row][curVertex.col] = True
#                     distArray[nextVertex.row][nextVertex.col] = nextVertex
#                     queue.append(nextVertex)
#     endVertex = distArray[h-1][w-1]
#     if endVertex.distance is None:
#         return endVertex.wallDistance
#     else:
#         return min(endVertex.distance, endVertex.wallDistance)

def solution(map):
    h = len(map)
    w = len(map[0])
    minLen = h + w - 1
    startVertex = Vertex(0, 0, 1)
    endVertex = Vertex(h - 1, w - 1, 1)
    # only cardinal directions allowed
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    forwardSearch = BFSState(map, startVertex, h-1, w-1)
    reverseSearch = BFSState(map, endVertex, 0, 0)
    shortestPath = None
    while len(forwardSearch.queue) > 0 and len(reverseSearch.queue) > 0:
        if len(forwardSearch.queue) > 0 and len(forwardSearch.seenList) < len(reverseSearch.seenList):
            # print "Forward"
            forwardSearch.step(moves)
        else:
            # print "Reverse"
            reverseSearch.step(moves)
        for vertex in forwardSearch.seenList:
            if reverseSearch.seenVertex[vertex.row][vertex.col]:
                newMin = vertex.distance + reverseSearch.distArray[vertex.row][vertex.col].distance - 1
                shortestPath = min(newMin, shortestPath) if shortestPath is not None else newMin
        for vertex in reverseSearch.seenList:
            if forwardSearch.seenVertex[vertex.row][vertex.col]:
                newMin = vertex.distance + forwardSearch.distArray[vertex.row][vertex.col].distance - 1
                shortestPath = min(newMin, shortestPath) if shortestPath is not None else newMin
    return shortestPath
    # else:
    #     endVertex = Vertex(h-1, w-1, 1)
    #     reverseSearch.findShortestPath(moves);
    #     remodelPathLen = forwardMinPath
    #     # we go through the list of reacheable walls
    #     # shortest distance to end = distance to wall + distance from end
    #     for wall in forwardSearch.wallVertices:
    #         if reverseSearch.seenVertex[wall.row][wall.col]:
    #             reverseDistance = reverseSearch.distArray[wall.row][wall.col].distance
    #             newPathLen = wall.distance + reverseDistance - 1
    #             remodelPathLen = min(newPathLen, remodelPathLen)
    #     return min(remodelPathLen, forwardMinPath)

class Vertex:
    def __init__(self, row, col, distance, wallDistance = None, passedWallCnt = 0):
        self.row = row
        self.col = col
        self.distance = distance
        self.wallDistance = wallDistance
        self.passedWallCnt = passedWallCnt
    def __str__(self):
        return "Distance:" + str(self.distance)
    def __repr__(self):
        return str(self)

class BFSState:
    def __init__(self, map, startVertex, endRow, endCol):
        self.map = map
        self.h = len(map)
        self.w = len(map[0])
        # we save the distances we have encountered
        # even wall distances should be saved
        self.distArray = [[None] * self.w for i in xrange(self.h)]
        # keep track of which vertices have alr been visited before
        self.seenVertex = [[False] * self.w for i in xrange(self.h)]
        self.seenList = []
        # we use bfs to determine shortest length
        self.queue = deque([startVertex])
        self.seenVertex[startVertex.row][startVertex.col] = True
        self.distArray[startVertex.row][startVertex.col] = startVertex
        self.endRow = endRow
        self.endCol = endCol

    def step(self, moves):
        nextVertex = self.queue.popleft()
        # vertices and their weights are added to dist and seen
        # walls should be added too
        for move in moves:
            adjRow = nextVertex.row + move[0]
            adjCol = nextVertex.col + move[1]
            if self.isOutOfBounds(adjRow, adjCol) or self.seenVertex[adjRow][adjCol]:
                continue
            curVertex = Vertex(adjRow, adjCol, nextVertex.distance + 1)
            self.seenVertex[adjRow][adjCol] = True
            self.seenList.append(curVertex)
            self.distArray[adjRow][adjCol] = curVertex

            if self.map[adjRow][adjCol] == 0:
                self.queue.append(curVertex)
        # print self.distArray

    def isOutOfBounds(self, row, col):
        return row < 0 or row >= self.h or col < 0 or col >= self.w

    def isEnd(self, row, col):
        return self.endRow == row and self.endCol == col

    def reachedEnd(self):
        return self.seenVertex[self.endRow][self.endCol]

    def getShortestPath(self):
        endVertex = self.distArray[self.endRow][self.endCol]
        if endVertex is None:
            raise Exception("Should not be unsolvable!")
        else:
            return endVertex.distance

print solution(
[[0,1,0,0,0],
[0,1,1,1,0],
[0,0,0,1,0],
[1,1,0,1,0],
[0,0,0,1,0],
[0,1,1,1,0],
[0,0,0,0,0]])

print solution([
    [0,1,0,0,0],
    [0,0,0,1,0],
    [1,1,1,1,0],
    [1,1,0,0,0],
    [1,1,0,1,0],
    [1,1,0,1,1],
    [1,1,0,0,0]
])

print solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])

print solution([
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
])

print solution([
    [0,1,0,0,0,1,0,0,0,1],
    [0,0,0,1,0,0,0,1,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,0,1],
    [0,1,1,1,1,1,1,1,0,0],
])

print solution([
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,0],
    [0,1,0,1,1,1,1,0],
    [0,1,0,1,1,1,1,0],
    [0,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,1,0]
])