# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visited = set() #set to track visited coords
    actionMem = list() #list of actions to take
    stck = util.Stack() #use given LIFO stack
    start = (problem.getStartState(),[]) #start with a tuple
   # print "Start: ", start
   # print "Is the start a goal?", problem.isGoalState(start)
    #print "Start's successors:", problem.getSuccessors(start)
    #print "last succ: ", problem.getSuccessors(start)[len(problem.getSuccessors(start)) - 1]

    
    stck.push(start) #push starting node into stack

    while not stck.isEmpty():
        node = stck.pop()
       # print "node: ", node
        actionMem = node[1]
       # print "actionMem: ", actionMem
# check node to see if visited and if it is our goal
        if node[0] not in visited:
            visited.add(node[0])
            if problem.isGoalState(node[0]): #iff goal return our mem
                return actionMem 
# check "neighbors", if they arent visited yet push them to stack
        for newnode in problem.getSuccessors(node[0]):
            if newnode[0] not in visited:
               # print "newnode: ", newnode
                stck.push((newnode[0], actionMem + [newnode[1]]))


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #same as above but queue
    visited = set() #set to track visited coords
    actionMem = list() #list of actions to take
    Q = util.Queue() #use given FIFO queue
    start = (problem.getStartState(),[]) #start with a tuple
    
    node = start
    Q.push(node)
    while not Q.isEmpty():
        node = Q.pop()
        actionMem = node[1]
        if node[0] not in visited:
            visited.add(node[0])
        if problem.isGoalState(node[0]):
            return actionMem
        #print "node: ", node
        #print "actionMem: ", actionMem
        for child in problem.getSuccessors(node[0]):
           # print "Child: ", child
            if child[0] not in visited:
                visited.add(child[0])
                Q.push((child[0], actionMem + [child[1]]))

       

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #similar to best first/dfs but track costs using given heaps
    
    visited = set() #set to track visited coords
    actionMem = list() #list of actions to take
    pq = util.PriorityQueue() #use given prio que (which involves heaps)
    start = (problem.getStartState(),[]) #start with a tuple

    #print "start: ", start

    
    pq.push(start, 0) #push starting node into heap que (heapq.heappush) [wants more than just start]
    #print "pq: ", pq

    while not pq.isEmpty():
        node = pq.pop()  #heap pop
        #print "node: ", node
        
        
        actionMem = node[1]
        #print "getcost: ", problem.getCostOfActions(node[1])
        
        if problem.isGoalState(node[0]): #iff goal return our mem
                return actionMem
        
        if node[0] not in visited:
            visited.add(node[0])
             
# check "neighbors", if they arent visited and arent in the heap yet push them to heap
        for newnode in problem.getSuccessors(node[0]):
            if newnode[0] not in visited and (newnode[0] not in (oldnode[2][0] for oldnode in pq.heap)):
               # print "newnode: ", newnode
               # print "newnode[1]: ", newnode[1]
   
                curCost = problem.getCostOfActions(actionMem + [newnode[1]])
                #print "curCost: ", curCost
                pq.push((newnode[0], actionMem + [newnode[1]]), curCost)
              #if pos is in heap check if current cost is higher than new cost for node and update heap if so  
            elif newnode[0] not in visited and (newnode[0] in (oldnode[2][0] for oldnode in pq.heap)):
                for oldnode in pq.heap:
                    if oldnode[2][0] == newnode[0]:
                        ocost = problem.getCostOfActions(oldnode[2][1]) #get old cost from heap
                        ncost = problem.getCostOfActions(actionMem + [newnode[1]]) #check new cost
                        if ncost < ocost:
                            pq.update((newnode[0], actionMem + [newnode[1]]), ncost) #updates priority and rebuilds heap (heapq.heapify)
               # print "visited already"
               # print "heap stuff: ", oldnode[2][0] 

                    

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    #i dont need to touch this
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #best first but f(n) = g(n) + h(n) where g(n) path cost from the initial state to node n, and h(n) is the estimated cost of the shortest path from n to a goal state
    #so start with ucs but use heuristic to comp cost

    visited = set() #set to track visited coords
    actionMem = list() #list of actions to take
    pq = util.PriorityQueue() #use given prio que (which involves heaps)
    start = (problem.getStartState(),[]) #start with a tuple

    #print "start: ", start

    
    pq.push(start, 0) #push starting node into heap que (heapq.heappush) [wants more than just start]
    #print "pq: ", pq

    while not pq.isEmpty():
        node = pq.pop()  #heap pop
        #print "node: ", node
        
        
        actionMem = node[1]
        #print "getcost: ", problem.getCostOfActions(node[1])
        
        if problem.isGoalState(node[0]): #iff goal return our mem
                return actionMem
        
        if node[0] not in visited:
            visited.add(node[0])
             
# check "neighbors", if they arent visited and arent in the heap yet push them to heap
        for newnode in problem.getSuccessors(node[0]):
            if newnode[0] not in visited and (newnode[0] not in (oldnode[2][0] for oldnode in pq.heap)):
               # print "newnode: ", newnode
               # print "newnode[1]: ", newnode[1]
   
                curCost = problem.getCostOfActions(actionMem + [newnode[1]])
                #print "curCost: ", curCost + heuristic(newnode[0], problem)
                pq.push((newnode[0], actionMem + [newnode[1]]), (curCost + heuristic(newnode[0], problem)))
              #if pos is in heap check if current cost is higher than new cost for node and update heap if so  
            elif newnode[0] not in visited and (newnode[0] in (oldnode[2][0] for oldnode in pq.heap)):
                for oldnode in pq.heap:
                    if oldnode[2][0] == newnode[0]:
                        ocost = problem.getCostOfActions(oldnode[2][1]) #get old cost from heap
                        ncost = problem.getCostOfActions(actionMem + [newnode[1]]) #check new cost
                        if ncost < ocost:
                            pq.update((newnode[0], (actionMem + [newnode[1]])), ncost + heuristic(newnode[0], problem)) #updates priority and rebuilds heap (heapq.heapify)
               # print "visited already"
               # print "heap stuff: ", oldnode[2][0] 


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
