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
import node

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

    frontier = util.Stack()
    explored_states = list()
    # was having problems with coordinates and out of range indexing so translate to tuple
    start_state = node.Node(problem.getStartState(), '', '')
    frontier.push(start_state)

    while True:
        # loop invariant
        if frontier.isEmpty():
            return False;

        # pop a node off the frontier
        current_node = frontier.pop()

        # check if current node is in goal state, return the path to the goal state node
        if problem.isGoalState(current_node.state):
            return current_node.path()

        # add current node to visited nodes and get list of successors
        successors_list = current_node.expand(problem)
        explored_states.append(current_node.state)

        # iterate through each of the successor nodes of the current node
        for elem in successors_list:
            # check if node is already been visited, else push to fringe
            if elem.state not in explored_states:
                frontier.push(node.Node(elem.state, current_node, elem.action, elem.path_cost))


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    explored_nodes = list()
    frontier = util.Queue()
    starting_node = node.Node(problem.getStartState())

    # check if starting node is already the goal state
    if problem.isGoalState(starting_node.state):
        return starting_node.path()

    frontier.push(starting_node)

    while True:
        # loop invariant
        if frontier.isEmpty():
            return False;

        # pop a node off the frontier
        current_node = frontier.pop()

        # check if current node is in goal state, return the path to the goal state node
        if problem.isGoalState(current_node.state):
            return current_node.path()

        # having trouble with for loop and conditional still adding visited elements
        if current_node.state not in explored_nodes:
            explored_nodes.append(current_node.state)

            # expand these now
            for child_node in current_node.expand(problem):
                if child_node.state not in explored_nodes:
                    frontier.push(node.Node(child_node.state, current_node, child_node.action))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    explored_nodes = list()
    frontier = util.PriorityQueue()
    frontier.push(node.Node(problem.getStartState()), 0.0)
    total_cost = 0.0

    while True:
        if frontier.isEmpty():
            return False

        current_node = frontier.pop()

        if problem.isGoalState(current_node.state):
            return current_node.path()

        if current_node.state not in explored_nodes:
            explored_nodes.append(current_node.state)

            for child in current_node.expand(problem):
                if child.state not in explored_nodes:
                    frontier.update(node.Node(child.state, current_node, child.action, current_node.path_cost), problem.getCostOfActions(child.path()))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
