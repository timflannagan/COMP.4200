# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Extract information from the GameState (initially not used in starter code)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        """
        Current problems/To-Do:
        [x] pacman constantly stopping in-place
        [x] use manhattanDistance instead of manual abs
        [ ] implement linear evaluation function
        [ ] implement capsules
        [ ] stop pacman bounces around in the same spot when food is near walls
        [ ] discourage going opposite direction from far away food
        [ ] fix returning only calculated_score without constantly losing
        """

        calculated_score = 0
        closest_food = None

        # iterate through the list of food to determine the closest food position
        for food in newFood.asList():
            distance_to_food = util.manhattanDistance(food, newPos)

            if not closest_food:
                closest_food = distance_to_food
            elif (distance_to_food < closest_food):
                closest_food = distance_to_food

        # play around with weights
        if (closest_food < 1):
            if currentGameState.getNumFood() <= successorGameState.getNumFood():
                calculated_score -= 100
            else:
                calculated_score += 50
        elif (closest_food < 5):
            calculated_score += 40
        elif (closest_food < 8):
            calculated_score += 35
        else:
            calculated_score += 20

        # had a problem where pacman would constantly stop in place
        if action == Directions.STOP:
            calculated_score -= 20

        # discourage going to the same location as the ghost
        if (newPos == newGhostStates[0].getPosition() and action == newGhostStates[0].getDirection()):
            calculated_score -= 50

        return calculated_score + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    best_moves = set()

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        """
        Note: should use self.depth, self.evaluationFunction
        Current Problems/To-do:
        1. Need to track depth so maximum depth isn't reached.
           - This could probably be achieved by comparing the depth of the current
             node with the initial depth: if (depth > self.depth): -> evaluate the state
        2. Modify minimax to be modular so it can handle more than two agent
        """

        def minimax(game_state, depth, agent_type):
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return self.evaluationFunction(game_state)

            available_moves = game_state.getLegalActions()
            best_move = available_moves[0]

            if agent_type == 0 or agent_type == game_state.getNumAgents():
                v = float('-inf')

                for move in game_state.getLegalActions():
                    successor = game_state.generateSuccessor(0, move)
                    v_prime = minimax(successor, depth, agent_type + 1)

                    if v_prime > v:
                        v = v_prime
                        best_move = move

                self.best_moves.add((game_state, best_move, v))
                return v
            else:
                v = float('inf')

                for move in game_state.getLegalActions(agent_type):
                    successor = game_state.generateSuccessor(agent_type, move)
                    v_prime = minimax(successor, depth - 1, agent_type + 1)

                    if v > v_prime:
                        v = v_prime
                        best_move = move

                self.best_moves.add((game_state, best_move, v))
                return v

        v = minimax(gameState, self.depth, 0)

        for parent, key, value in self.best_moves:
            if key in gameState.getLegalActions() and value == v and parent == gameState:
                return key

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    best_moves = set()

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alpha_beta(game_state, depth, alpha, beta, agent_type):
            """
            minimax algorithm based off wikipedia's pseudocode
            """
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return self.evaluationFunction(game_state)

            best_move = game_state.getLegalActions()[0]

            # check if the current agent type is a maximum or minimum agent
            if agent_type == 0 or agent_type == game_state.getNumAgents():
                v = float('-inf')

                for move in game_state.getLegalActions():
                    successor = game_state.generateSuccessor(agent_type, move)

                    v_prime = alpha_beta(successor, depth, alpha, beta, agent_type + 1)

                    if v_prime > v:
                        v = max(v, v_prime)
                        best_move = move

                    alpha = max(alpha, v)

                    if beta < v:
                        break

                self.best_moves.add((game_state, best_move, v))
                return v
            else:
                """
                here agent_type could be anything between 1 <= agent_type <= game_state.getNumAgents()
                0 -> pacman/max node
                1 <= agent_type <= game_state.getNumAgents() -> min node
                """
                v = float('inf')

                # iterate through available moves from the current agent type
                for move in game_state.getLegalActions(agent_type):
                    successor = game_state.generateSuccessor(agent_type, move)
                    v_prime = alpha_beta(successor, depth - 1, alpha, beta, agent_type + 1)

                    if v_prime < v:
                        v = min(v, v_prime)
                        best_move = move

                    beta = min(beta, v)

                    if alpha > v:
                        break

                self.best_moves.add((game_state, best_move, v))
                return v

        v = alpha_beta(gameState, self.depth, float('-inf'), float('inf'), 0)

        for parent, key, value in self.best_moves:
            if key in gameState.getLegalActions() and value == v and parent == gameState:
                return key

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
