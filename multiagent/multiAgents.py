# multiAgents.py
# --------------
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
        currentGameState = currentGameState.generatePacmanSuccessor(action)
        pacmanPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodList = newFood.asList()
        min_food_distance = -1
        ghost_material_value = 0
        for food in newFoodList:
            distance = util.manhattanDistance(pacmanPos, food)
            if min_food_distance >= distance or min_food_distance == -1:
                min_food_distance = distance
        for newGhostState in newGhostStates:
            if util.manhattanDistance(pacmanPos, newGhostState.getPosition()) <= 1:
              ghost_material_value = -1000 
        return currentGameState.getScore() + 1 * (1 / float(min_food_distance)) + 1 * (ghost_material_value)

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

        legalMoves = gameState.getLegalActions(0) # print gameState
        # print (self.depth)
        # scores = [self.get_value(gameState, 0, action, gameState.getNumAgents() * self.depth) for action in legalMoves]
        successors = [gameState.generateSuccessor(0, action) for action in legalMoves]
        scores = [self.minimax(1, successor, 0) for successor in successors]

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0] # chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    # def minimax(self, state, agentIndex, action, n_depth):
    #     return None

    def minimax(self, agentIndex, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maximize(agentIndex, gameState, depth)
        else:
            return self.minimize(agentIndex, gameState, depth)

    def maximize(self, agentIndex, gameState, depth):
        nextAgent = agentIndex + 1

        # for action in gameState.getLegalActions(0):
        #     succ = gameState.generateSuccessor(0, action)
        #     tmp = self.minimize(succ, depth, 1, numGhosts, )
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        scores = [self.minimax(nextAgent, successor, depth) for successor in successors]

        return max(scores)

    def minimize(self, agentIndex, gameState, depth):
        nextAgent = agentIndex + 1
        if gameState.getNumAgents() == nextAgent:
            nextAgent = 0
            depth += 1
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        scores = [self.minimax(nextAgent, successor, depth) for successor in successors]
        # for action in gameState.getLegalActions(0):
        #     succ = gameState.generateSuccessor(0, action)
        #     tmp = self.minimize(succ, depth, 1, numGhosts, )
        
        # if agentIndex == gameState.getNumAgents():
        #     actions = gameState.getLegalActions(agentIndex)
        #     successors = [gameState.generateSuccessor(agentIndex + 1, action) for action in actions]
        #     scores = [self.minimize(successor, depth, agentIndex + 1) for successor in successors]
        # else:
        #     actions = gameState.getLegalActions(0)
        #     successors = [gameState.generateSuccessor(0, action) for action in actions]
        #     scores = [self.maximize(successor, depth + 1) for successor in successors]

        return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float('-inf')
        beta = float('inf')
        utility = float('-inf')
        legalMoves = gameState.getLegalActions(0) 
        for action in legalMoves:
            successors = [gameState.generateSuccessor(0, action)]
            agentValue = max([self.alphabeta(1, successor, 0, alpha, beta) for successor in successors])
            if agentValue > utility:
              utility = agentValue
              bestAction = action

            alpha = max(alpha, utility)

        return bestAction
        # scores = [self.alphabeta(1, successor, 0, alpha, beta) for successor in successors]

        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = bestIndices[0] # chosenIndex = random.choice(bestIndices)
        # return legalMoves[chosenIndex]

    # def alphabeta(self, state, agentIndex, action, n_depth):
    #     return None

    def alphabeta(self, agentIndex, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maximize(agentIndex, gameState, depth, alpha, beta)
        else:
            return self.minimize(agentIndex, gameState, depth, alpha, beta)

    def maximize(self, agentIndex, gameState, depth, alpha, beta):
        v = float('-inf')
        nextAgent = agentIndex + 1

        # for action in gameState.getLegalActions(0):
        #     succ = gameState.generateSuccessor(0, action)
        #     tmp = self.minimize(succ, depth, 1, numGhosts, )
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successors = [gameState.generateSuccessor(agentIndex, action)]
            scores = [self.alphabeta(nextAgent, successor, depth, alpha, beta) for successor in successors]
            v = max(scores)
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def minimize(self, agentIndex, gameState, depth, alpha, beta):
        v = float('inf')

        nextAgent = agentIndex + 1
        if gameState.getNumAgents() == nextAgent:
            nextAgent = 0
            depth += 1
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successors = [gameState.generateSuccessor(agentIndex, action)]
            scores = [self.alphabeta(nextAgent, successor, depth, alpha, beta) for successor in successors]
            v = min(scores)
            if v < alpha:
                return v
            beta = min(v, beta)
        return v

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
        legalMoves = gameState.getLegalActions(0) # print gameState
        # print (self.depth)
        # scores = [self.get_value(gameState, 0, action, gameState.getNumAgents() * self.depth) for action in legalMoves]
        successors = [gameState.generateSuccessor(0, action) for action in legalMoves]
        scores = [self.minimax(1, successor, 0) for successor in successors]

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0] # chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        # util.raiseNotDefined()

    def minimax(self, agentIndex, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maximize(agentIndex, gameState, depth)
        else:
            return self.minimize(agentIndex, gameState, depth)

    def maximize(self, agentIndex, gameState, depth):
        nextAgent = agentIndex + 1

        # for action in gameState.getLegalActions(0):
        #     succ = gameState.generateSuccessor(0, action)
        #     tmp = self.minimize(succ, depth, 1, numGhosts, )
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        scores = [self.minimax(nextAgent, successor, depth) for successor in successors]

        return max(scores)

    def minimize(self, agentIndex, gameState, depth):

        nextAgent = agentIndex + 1
        if gameState.getNumAgents() == nextAgent:
            nextAgent = 0
        if nextAgent == 0:
            depth += 1
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
        scores = [self.minimax(nextAgent, successor, depth) for successor in successors]
        # for action in gameState.getLegalActions(0):
        #     succ = gameState.generateSuccessor(0, action)
        #     tmp = self.minimize(succ, depth, 1, numGhosts, )
        
        # if agentIndex == gameState.getNumAgents():
        #     actions = gameState.getLegalActions(agentIndex)
        #     successors = [gameState.generateSuccessor(agentIndex + 1, action) for action in actions]
        #     scores = [self.minimize(successor, depth, agentIndex + 1) for successor in successors]
        # else:
        #     actions = gameState.getLegalActions(0)
        #     successors = [gameState.generateSuccessor(0, action) for action in actions]
        #     scores = [self.maximize(successor, depth + 1) for successor in successors]

        return sum(scores) / len(scores)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # currentGameState = currentGameState.generatePacmanSuccessor(action)
    pacmanPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    newFoodList = newFood.asList()
    min_food_distance = -1
    for food in newFoodList:
        distance = util.manhattanDistance(pacmanPos, food)
        if min_food_distance >= distance or min_food_distance == -1:
            min_food_distance = distance
    ghost_material_value = 0
    for newGhostState in newGhostStates:
        if util.manhattanDistance(pacmanPos, newGhostState.getPosition()) <= 1:
          ghost_material_value = -1000 
    return currentGameState.getScore() + 1 * (1 / float(min_food_distance)) + 1 * (ghost_material_value)

# Abbreviation
better = betterEvaluationFunction

