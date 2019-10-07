# this file should contain an implementation of a low-level state vector

# tentatively, using numpy arrays for vectors
import numpy
from numpy import array
from solitaire import Game

class LowLevelVector:
    # vector keeps track of its game and updates itself from the game
    #numpy array representation
    #1: feature that is always 1 for weight stuff
    #2-5: number face-up cards in block piles
    #6-12: number face-up cards in each play pile
    #keep corresponding weight array of feature vector
    def __init__(self, game):
        self.game = game
        lowLevelVector = numpy.array([1,0,0,0,0,1,1,1,1,1,1,1])
        lowLevelWeights = numpy.array([1,1,1,1,1,1,1,1,1,1,1,1])
        self.update(self.game.getGameElements())

    #update feature vector
    #DO NOT update first value- always keep at 1
    def update_features(self, state, action):
        # this method should update the vector according to the game elements "printout" received from self.game
        # implementation will depend on what we do for features

        # TODO: syntax issues, block and playpiles are backwards
        gameElements = state.getGameElements()
        blockPiles = gameElements(1)
        i=1
        for pile in blockPiles:
            self.lowLevelVector[i] = len(pile)

        # get number of flipped cards in each play pile and update
        playPiles = gameElements(2)
        i = 5
        for pile in playPiles:
            self.lowLevelVector[i] = len(pile.getFlippedCards())

        pass

    #TODO update weight array with gradient stuff
    def update_weights(self,alpha,gamma,reward):

        for i in range(len(self.lowLevelWeights)):
            self.lowLevelWeights[i] += self.lowLevelWeights[i] + alpha(reward +)



    #get Q using linear function approximation
    #if Q is in terminating state, either by out of moves or winning, return 0
    def get_Q(self,state,action):

        #if action id is -1 (i.e. no possible moves) return 0
        if action.id == -1:
            return 0

        #if game is won retun 0
        if state.checkIfCompleted():
            return 0

        #update features based on new state
        self.update_features(state,action)

        #sum all weights*features
        Q = 0
        for i in range(self.lowLevelVector):
            Q += self.lowLevelVector[i]*self.lowLevelWeights[i]

        return Q



