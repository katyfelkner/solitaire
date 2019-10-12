import numpy
from numpy import array
from solitaire import Game

class HighLevelVector:

    # vector keeps track of its game and updates itself from the game
    #numpy array representation
    #1: feature that is always 1 for weight stuff
    #2: number valid moves
    #3-6: lowest card value on each play pile
    #7-13: highest card in each block
    def __init__(self):
        self.HighLevelFeatures = numpy.array([1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.HighLevelWeights = numpy.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])

    #update feature vector
    #DO NOT update first value- always keep at 1
    def update_features(self, state):
        # this method should update the vector according to the game elements "printout" received from self.game
        # implementation will depend on what we do for features

        numPossibleMoves = len(state.getPossibleMoves())
        self.HighLevelFeatures[1]=numPossibleMoves

        gameElements = state.getGameElements()
        blockPiles = gameElements.get("blockPiles")
        i=2

        for key in blockPiles.keys():
            pile = blockPiles.get(key)
            if len(pile.cards)==0:
                self.HighLevelFeatures[i]=0
            else:
                val = pile.cards[-1].value
                if val == 'K':
                    val = 13
                elif val == 'J':
                    val = 11
                elif val == 'Q':
                    val = 12
                elif val == 'A':
                    val = 1
                self.HighLevelFeatures[i] = val
            i += 1


        # get number of flipped cards in each play pile and update
        playPiles = gameElements.get("playPiles")
        i = 6
        for pile in playPiles:
            if len(pile.cards)==0:
                self.HighLevelFeatures[i]=0
                i+=1
                continue

            val = pile.cards[0].value
            if val == 'K':
                val = 13
            elif val == 'J':
                val = 11
            elif val == 'Q':
                val = 12
            elif val == 'A':
                val = 1
            self.HighLevelFeatures[i] = val
            i += 1

    def update_weights(self,alpha, delta):
        for i in range(len(self.HighLevelWeights)):
            test = alpha * delta * self.HighLevelFeatures[i]
            self.HighLevelWeights[i] += test
            self.HighLevelWeights[i] /= 10


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
        for i in range(len(self.HighLevelFeatures)):
            Q += self.HighLevelFeatures[i]*self.HighLevelWeights[i]

        return Q
