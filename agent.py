from solitaire import Game
from high_level_vector import HighLevelVector
from low_level_vector import LowLevelVector
from action import Action
from numpy import array
import numpy as np

#Function to choose what action to take next, depending on next state and epsilon
#@return next action
def epsilon_greedy(features,state,epsilon):

    #find all valid moves that can be made- returns list of action objects
    possible_moves = state.getPossibleMoves()

    if len(possible_moves) == 0:
        return Action(None,None,None,-1)

    #get random number between 1-10
    #if random number > epsilon*10 choose an action at random
    random_chance = np.random.randint(1,11)
    if random_chance > epsilon*10:
        random_choice = np.random.randint(0,len(possible_moves))
        return possible_moves[random_choice]

    #else choose move with highest Q value
    #if there are multiple actions with the max Q value, choose one of them at random
    Q_vals = []
    for i in range(len(possible_moves)):
        Q_vals.append(features.get_Q(state,possible_moves[i]))

    maxVal = max(Q_vals)
    maxIndices = [i for i, j in enumerate(Q_vals) if j == maxVal]

    #maxReward = max(rewards)
    #maxIndices = [i for i, j in enumerate(rewards) if j==maxReward]
    MaxIndex = np.random.randint(0,len(maxIndices))
    return possible_moves[MaxIndex]

"""
@param alpha- learning rate
@param gamma - discount factor
@param epsilon  - exploration
@param num_games - number games for training
@param max_moves - maximum moves until game is considered a loss
"""
def SARSA(alpha, gamma, epsilon, num_games, max_moves,high_level,f_moves,f_scores,f_wins):

    global won, total_score, moves
    total_moves = []
    final_scores = []
    wins = []

    #Get initial Q, depending on whether high or low level features
    if high_level:
        features = HighLevelVector()
    else:
        features = LowLevelVector()

    for game in range(num_games):

        won = False
        print("Game number {0}".format(game))
        total_score = 0
        moves = 0

        #get initial state, action, Q, based on new game
        state = Game()
        action = epsilon_greedy(features,state,epsilon)

        while moves < max_moves:

            #Get Q(s,a) before state gets updated with make move
            Q_init = features.get_Q(state, action)

            #make a move, update state and total score
            # state automatically updates when making a move, no need to manually update value
            reward = state.make_move(action)
            total_score += reward
            moves += 1

            #get next action using epsilon greedy and corresponding Q
            next_action = epsilon_greedy(features,state,epsilon)
            Q_next = features.get_Q(state,next_action)
            delta = reward + gamma*Q_next - Q_init
            features.update_weights(alpha,delta)

            #Update Q, feature weights, state, action
            action = next_action

            #If in terminal state (either won, can't move, or exceed move limit) break out of while loop
            if Q_next == 0 or moves >= max_moves:
                if state.checkIfCompleted():
                    won = True
                    print("nice")
                else:
                    print("not nice")
                break

        #Update score and wins/losses list based off of win/loss
        if won:
            total_score += 1000
            wins.append(1)
            #f_wins.write("1, ")
        else:
            total_score -= 1000
            wins.append(0)
            #f_wins.write("0, ")


        # print("score: " + str(total_score) + ", moves: " + str(total_moves) + ",won: " + str(won) )
        total_moves.append(moves)
        final_scores.append(total_score)

        #f_moves.write(str(moves))
        #f_moves.write(", ")
        #f_scores.write(str(total_score))
        #f_scores.write(", ")

    return total_moves, final_scores, wins

def agent():

    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.9
    EPSILON = 0.9
    NUM_TRAINING_GAMES = 100
    MOVE_LIMIT = 500
    HIGH_LEVEL = False

    f_moves = open("low_total_moves.txt","a")
    f_scores = open("low_final_scores.txt","a")
    f_wins = open("low_wins.txt","a")

    total_moves, final_scores, wins = SARSA(LEARNING_RATE,DISCOUNT_FACTOR,EPSILON,NUM_TRAINING_GAMES,MOVE_LIMIT,HIGH_LEVEL,f_moves,f_scores,f_wins)

    # print(total_moves)
    # print(final_scores)
    # print(wins)

    f_moves.close()
    f_scores.close()
    f_wins.close()


if __name__ == "__main__":
    agent()
