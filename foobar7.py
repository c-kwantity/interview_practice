"""
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and relieved the bunnies of their work duries -- and now you need to escape from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time.

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can fit through at a time in each direction of every corridor in between, figure out how many bunnies can safely make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of integers denoting where the groups of gathered bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most 2000000 bunnies that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.  (Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains the same.)
"""
from collections import deque

def solution(entrances, exits, path):
    if len(entrances) <= 0 or len(exits) <= 0:
        return 0
    maxPossible = 2000000
    # extra nodes added as source and sinks
    flowGraph = createFlowGraph(entrances, exits, path, maxPossible)
    while True: #will break based on curPath
        curPath = getPath(flowGraph, maxPossible)
        if curPath is None: # only from source
            break # no more paths available
        updateFlowGraph(flowGraph, curPath)
    flow = 0
    for node in flowGraph:
        flow += node[len(node) - 1].flow #add all the flows going to the last node
    return flow

def getPath(flowGraph, maxFlow):
    stack = deque([Path(0, [0], maxFlow)])
    sinkNode = len(flowGraph) - 1
    seen = set()
    while len(stack) > 0:
        curPath = stack.pop()
        currentRoom = curPath.room
        prevPath = curPath.path
        curCapacity = curPath.capacity
        if currentRoom == sinkNode:
            return curPath # we stop after finding a path to sink
        seen.add(currentRoom)
        for i in xrange(len(flowGraph[currentRoom])): # from the source
            path = list(prevPath)
            if i in seen:
                continue
            curNode = flowGraph[currentRoom][i]
            if curNode.capacity > curNode.flow: #add node if forward flow is possible
                path.append(i)
                stack.append(Path(i, path, min(curCapacity, curNode.capacity - curNode.flow)))
            backNode = flowGraph[i][currentRoom] # also add node if reverse flow if possible
            if backNode.flow > 0:
                path.append(i)
                stack.append(Path(i, path, min(curCapacity, backNode.flow)))
    return None


def updateFlowGraph(flowGraph, pathAndCapacity):
    curPath = pathAndCapacity.path
    minCapacity = pathAndCapacity.capacity
    for i in (xrange(len(curPath) - 1)):
        source = curPath[i]
        dest = curPath[i+1]
        curNode = flowGraph[source][dest]
        if curNode.capacity > 0:
            flowGraph[source][dest].flow += minCapacity
        else:
            flowGraph[dest][source].flow -= minCapacity
    return minCapacity

def createFlowGraph(entrances, exits, path, maxPossible):
    flowGraphLen = len(path) + 2 #adding source and sink node
    flowGraph = [[FlowNode(0,0) for i in xrange(flowGraphLen)] for i in xrange(flowGraphLen)]
    for i in entrances:
        # entrances have max flow from source node to entrances
        flowGraph[0][i+1].capacity = maxPossible
    for i in exits:
        # exits have max flow from exit to sink
        flowGraph[i+1][flowGraphLen - 1].capacity = maxPossible
    for i in xrange(len(path)):
        for j in xrange(len(path[i])):
            flowGraph[i+1][j+1].capacity = path[i][j]
    return flowGraph

class FlowNode:
    def __init__(self, flow, capacity):
        self.flow = flow
        self.capacity = capacity
    def __str__(self):
        return str(self.flow) + "/" + str(self.capacity)
    def __repr__(self):
        return str(self)

class Path:
    def __init__(self, room, path, capacity):
        self.room = room
        self.path = path
        self.capacity = capacity

print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))
print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 1], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))