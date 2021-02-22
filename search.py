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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    stack = util.Stack()
    path = []
    visited = []
    stack.push(problem.getStartState())
    first = True
    parentMap = {}
    while not stack.isEmpty():
        node = stack.pop()
        if first:
            if problem.isGoalState(node):
                return path
            visited.append(node)
            successors = problem.getSuccessors(node)
            for successor in successors:
                if successor[0] not in visited:
                    stack.push(successor)
                    parentMap[successor] = node
            first = False
        else:
            if problem.isGoalState(node[0]):
                curr = node
                while curr in parentMap:
                    path.append(curr[1])
                    curr = parentMap[curr]
                path.reverse()
                return path
            visited.append(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                if successor[0] not in visited:
                    stack.push(successor)
                    parentMap[successor] = node
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    queue = util.Queue()
    path = []
    visited = []
    queue.push(problem.getStartState())
    first = True
    parentMap = {}
    while not queue.isEmpty():
        node = queue.pop()
        if first:
            if problem.isGoalState(node):
                return path
            visited.append(node)
            successors = problem.getSuccessors(node)
            for successor in successors:
                if successor[0] not in visited:
                    queue.push(successor)
                    visited.append(successor[0])
                    parentMap[successor] = node
            first = False
        else:
            if problem.isGoalState(node[0]):
                curr = node
                while curr in parentMap:
                    path.append(curr[1])
                    curr = parentMap[curr]
                path.reverse()
                return path
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                if successor[0] not in visited:
                    queue.push(successor)
                    visited.append(successor[0])
                    parentMap[successor] = node
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    pqueue = util.PriorityQueue()
    visited = set()
    path = []
    pqueue.push(problem.getStartState(), 0)
    first = True
    parentMap = {}
    while not pqueue.isEmpty():
        node = pqueue.pop()
        if first:
            visited.add(node)
            if problem.isGoalState(node):
                return path
            successors = problem.getSuccessors(node)
            for successor in successors:
                parentMap[successor]=(node,successor[2])
                pqueue.push(successor,successor[2])
            first = False
        else:
            if node[0] not in visited:
                visited.add(node[0])
                if problem.isGoalState(node[0]):
                    curr = node
                    while curr in parentMap:
                        path.append(curr[1])
                        curr = parentMap[curr][0]
                    path.reverse()
                    return path
                successors = problem.getSuccessors(node[0])
                for successor in successors:
                    if successor[0] not in visited:
                        if successor in parentMap and parentMap[successor][1] < parentMap[node][1] + successor[2]:
                            break
                        else:
                            parentMap[successor]=(node,parentMap[node][1] + successor[2])
                            pqueue.update(successor,parentMap[node][1] + successor[2])
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pqueue = util.PriorityQueue()
    visited = set()
    path = []
    pqueue.push(problem.getStartState(), 0)
    parentMap = {}
    first = True
    while not pqueue.isEmpty():
        node = pqueue.pop()
        if first:
            visited.add(node)
            if problem.isGoalState(node):
                return path
            successors = problem.getSuccessors(node)
            for successor in successors:
                parentMap[successor] = (node,successor[2])
                pqueue.push(successor,successor[2] + heuristic(successor[0],problem))
            first = False
        else:
            if node[0] not in visited:
                visited.add(node[0])
                if(problem.isGoalState(node[0])):
                    curr = node
                    while curr in parentMap:
                        path.append(curr[1])
                        curr = parentMap[curr][0]
                    path.reverse()
                    return path
                successors = problem.getSuccessors(node[0])
                for successor in successors:
                    if successor[0] not in visited:
                        if successor not in parentMap or parentMap[successor][1] > parentMap[node][1] + successor[2]:
                            parentMap[successor] = (node,parentMap[node][1] + successor[2])
                            pqueue.update(successor,parentMap[successor][1] + heuristic(successor[0], problem))
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
