from solitaire import Game
from high_level_vector import HighLevelVector
from low_level_vector import LowLevelVector
from action import Action
from numpy import array
import numpy as np

class agent:

    #Function to choose what action to take next, depending on next state and epsilon
    #@return next action
    def epsilon_greedy(self,state,epsilon):

        #find all valid moves that can be made- returns list of action objects
        possible_moves = state.getPossibleMoves()
        rewards = []

        if len(possible_moves) == 0:
            return Action(None,None,None,-1)

        #get rewards corresponding to all possible moves
        for i in range(len(possible_moves)):

            #if action is a move between piles, 0 reward (or 5 if a card is flipped as a result)
            if possible_moves[i].id == 1:
                if possible_moves[i].flipBonus:
                    rewards[i]=5
                else:
                    rewards[i] = 0

            #if action is a move from pile to block, 10 reward (or 15 if a card is flipped as a result)
            elif possible_moves[i].id == 2:
                if possible_moves[i].flipBonus:
                    rewards[i]=15
                else:
                    rewards[i] = 10

            #if action is a move from block to pile, -15 reward
            elif possible_moves[i].id == 3:
                rewards[i] = -15

            #if action is draw card, 0 reward
            elif possible_moves[i].id == 4:
                rewards[i] = 0

            #if action is recycle deck, -100 reward
            elif possible_moves[i].id == 5:
                rewards[i] = -100

            #if action is move from waste to pile, 5 reward
            elif possible_moves[i].id == 6:
                rewards[i] = 5

            #if action is move from waste to block, 10 reward
            elif possible_moves[i].id == 7:
                rewards[i] = 10

        #get random number between 1-10
        #if random number > epsilon*10 choose an action at random
        random_chance = np.random.randint(1,11)
        if random_chance > epsilon*10:
            random_choice = np.random.randint(0,len(possible_moves))
            return possible_moves[random_choice]

        #else choose move with hightest reward
        #if there are multiple actions with the max reward, choose one of them at random
        maxReward = max(rewards)
        maxIndices = [i for i, j in enumerate(rewards) if j==maxReward]
        randomMaxIndex = np.random.randint(0,len(maxIndices))
        return possible_moves[randomMaxIndex]

    """
    @param alpha- learning rate
    @param gamma - discount factor
    @param epsilon  - exploration
    @param num_games - number games for training
    @param max_moves - maximum moves until game is considered a loss
    """
    def SARSA(self, alpha, gamma, epsilon, num_games, max_moves,high_level):

        total_moves = []
        final_scores = []
        wins = []

        #Get initial Q, depending on whether high or low level features
        if high_level:
            features = HighLevelVector
        else:
            features = LowLevelVector

        for game in range(num_games):

            won = False
            #print("Game number {game}")
            total_score = 0
            moves = 0

            #get initial state, action, Q, based on new game
            state = Game()
            action = self.epsilon_greedy(state,epsilon)
            Q = features.get_Q(state,action)

            while moves < max_moves:

                #make a move, update state and total score
                # state automatically updates when making a move, no need to manually update value
                reward = state.make_move(action)
                total_score += reward
                moves += 1

                #get next action using epsilon greedy and corresponding Q
                next_action = self.epsilon_greedy(state,epsilon)
                next_Q = features.get_Q(state,next_action)

                #Update Q, feature weights, state, action
                Q += alpha*[reward+(gamma*next_Q-Q)]
                features.update_weights(alpha,gamma,reward)
                action = next_action

                #If in terminal state (either won, can't move, or exceed move limit) break out of while loop
                if next_Q == 0 or moves >= 500:
                    if game.checkIfCompleted():
                        won = True
                    break

            #Update score and wins/losses list based off of win/loss
            if won:
                total_score += 1000
                wins.append(1)
            else:
                total_score -= 1000
                wins.append(0)

            total_moves.append(moves)
            final_scores.append(total_score)

        return total_moves, final_scores, wins

    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.9
    EPSILON = 0.9
    NUM_TRAINING_GAMES = 10
    MOVE_LIMIT = 500
    HIGH_LEVEL = False

    total_moves, final_scores, wins = SARSA(LEARNING_RATE,DISCOUNT_FACTOR,EPSILON,NUM_TRAINING_GAMES,MOVE_LIMIT,HIGH_LEVEL)

    #TODO: use total move and final score data to do some graphing / analysis
