# node.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# THIS IS OFFICIAL SOLUTION CODE. DO NOT REDISTRIBUTE OUTSIDE CLASS.

class Node:
    "A Tree node data structure for doing searches"
    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree node, derived from a parent by an action"
        self.state = state
        self.parent = parent
        self.action = action
        if parent:
            "Node has a parent that is not null"
            self.path_cost = parent.path_cost + path_cost
            self.depth = parent.depth + 1
        else:
            "Beginning of the search"
            self.path_cost = path_cost
            self.depth = 0

    def __repr__(self):
        return "<Node: %s>" % (self.state,)

    def nodePath(self):
        "Creates a list of nodes from the root to this node"
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        result.reverse()
        return result

    def path(self):
        "Creates a path of actions from the start to the current state"
        actions = []
        currnode = self
        while currnode.parent:
            actions.append(currnode.action)
            currnode = currnode.parent
        actions.reverse()
        return actions

    def expand(self, problem):
        "Return a list of nodes reachable from this node [Fig. 3.8]"
        return [Node(next, self, act, cost)
                for (next, act, cost) in problem.getSuccessors(self.state)]
