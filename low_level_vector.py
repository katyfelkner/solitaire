# this file should contain an implementation of a Low-level state vector

# tentatively, using numpy arrays for vectors
from numpy import array
from solitaire import Game
import numpy

class LowLevelVector:

    # vector keeps track of its game and updates itself from the game
    #numpy array representation
    #1: feature that is always 1 for weight stuff
    #2-5: number face-up cards in block piles
    #6-12: number face-up cards in each play pile
    #keep corresponding weight array of feature vector
    def __init__(self):
        self.LowLevelFeatures = numpy.array([1,0,0,0,0,1,1,1,1,1,1,1])
        self.LowLevelWeights = numpy.array([1,1,1,1,1,1,1,1,1,1,1,1])

    #update feature vector
    #DO NOT update first value- always keep at 1
    def update_features(self, state):
        # this method should update the vector according to the game elements "printout" received from self.game
        # implementation will depend on what we do for features

        gameElements = state.getGameElements()
        blockPiles = gameElements.get("blockPiles")
        i=1

        for key in blockPiles.keys():
            pile = blockPiles.get(key)
            self.LowLevelFeatures[i]=len(pile.cards)
            i += 1

        # for pile in blockPiles:
        #     cards = pile.cards
        #     self.LowLevelFeatures[i] = len(cards)
        #     i += 1

        # get number of flipped cards in each play pile and update
        playPiles = gameElements.get("playPiles")
        i = 5
        for pile in playPiles:
            self.LowLevelFeatures[i] = len(pile.getFlippedCards())
            i += 1

    def update_weights(self,alpha, delta):
        for i in range(len(self.LowLevelWeights)):
            self.LowLevelWeights[i] += alpha*delta*self.LowLevelFeatures[i]


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
        self.update_features(state)

        #sum all weights*features
        Q = 0
        for i in range(len(self.LowLevelFeatures)):
            Q += self.LowLevelFeatures[i]*self.LowLevelFeatures[i]

        return Q

