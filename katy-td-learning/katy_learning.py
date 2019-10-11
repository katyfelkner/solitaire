"""QLearning():
  #initialization
  for each state s in AllNonTerminalStates:
     for each action a in Actions(s):
         Q(s,a) = random()
  for each s in TerminalStates:
      Q(s,_) = 0 #Q(s) = 0 for all actions in s
  Loop number_of_episodes:
    let s = start_state()
    # Play episode until the end
    Loop until game_over():
      # get action to perform on state s according
      # to the given policy 90% of the time, and a
      # random action 10% of the time.
      let a = get_epsilon_greedy_action(s, 0.1)
      # make move from s using a and get the new state s'
      # and the reward r
      let (s', r) = make_move(s, a)
      # choose the max Q-value (qmax) on state s'
      let qmax = get_max_qvalue_on_state(s')
      # incrementally compute the average at Q(s,a)
      let Q(s, a) = Q(s, a) + alpha*[r + gamma * qmax - Q(s, a)]"""



# implement TD learning slowly moving epsilon to 0 in order to approximate pi*

from solitaire import Game
import random

class QLearningAgent:

    def __init__(self, epsilon, gamma, alpha, moves, games):
        """
        Initialize a learning agent with the following features
        :param epsilon: initial epsilon. will be scaled down as time continues
        :param gamma: discount factor. Normal values are between .9 and .99
        :param alpha: learning rate. Norman values are around .1
        :param moves: limit on moves per game, to avoid infinite loops. 600 or so is reasonable.
        :param games: number of games on which to train. 10-50 for small-scale testing, several thousand for actual learning
        """
        self.INITIAL_EPSILON = epsilon
        self.GAMMA = gamma
        self.ALPHA = alpha
        self.MOVES_PER_GAME = moves
        self.NUM_GAMES = games
        self.weights = [1,1,1,1,1,1,1,1,1,1,1,1] # weights array, all init to one
        self.game = None
        self.feature_vector = None
        # we are assuming the low-level features for now
        # TODO: check this

    def decreasing_e_greedy(self, num_games, epsilon):
        """
        Apply an e-greedy policy with decreasing epsilon to choose next action.

        @:param num_games - number of games played so far
        @:param epsilon - initial epsilon
        @:param game - Game object representing current game state - this is NOT the state vector

        @:return next action - Action
        """

        # calculate scaled epsilon
        scaled_epsilon = epsilon * (self.NUM_GAMES - num_games) / self.NUM_GAMES

        # get all possible moves for the state
        possible_moves = self.game.getPossibleMoves()

        # if no possible moves, there is no action and we should return none
        if len(possible_moves) == 0:
            return None

        # epsilon % chance of selecting a random action
        if random.random() < scaled_epsilon:
            return random.choice(possible_moves)

            # else, choose based on a predicted q
        """
        max_q = None
        max_a = []
        for a in possible_moves:
            # calculate q(s, a)

            # TODO: this line is very wrong
            Q_a = self.game.get_predicted_reward(a) + self.GAMMA * sum(self.feature_vector[i] * self.weights[i] for i in range(len(self.feature_vector)))

            # compare to max
            if max_q is None or Q_a > max_q:
                max_q = Q_a
                max_a = [a]
            elif Q_a == max_q:
                # need to select randomly among equal q values
                max_a.append(a)

        """
        # else, choose based on a predicted q

        max_q = None
        max_a = []
        for a in possible_moves:
            # calculate q(s, a)
            try:
                reward, new_game = self.game.test_move(a)
                s_prime = self.get_features(new_game)

                Q_a = reward + self.GAMMA * sum(s_prime[i] * self.weights[i] for i in range(len(s_prime)))

                # compare to max
                if max_q is None or Q_a > max_q:
                    max_q = Q_a
                    max_a = [a]
                elif Q_a == max_q:
                    # need to select randomly among equal q values
                    max_a.append(a)
            except:
                # remove from set of legal moves
                possible_moves.remove(a)

        # return action with maximum q
        if len(max_a) == 0:
            return None
        else:
            return random.choice(max_a)

    def learn(self):

        total_moves = []
        final_scores = []
        wins = []

        # start looping over games
        for i in range(self.NUM_GAMES):
            # reinitialize feature vector and game object
            self.feature_vector = [1,0,0,0,0,1,1,1,1,1,1,1]
            self.game = Game()
            print(self.game.getGameElements())

            won = False
            print("Game number", i)
            total_score = 0
            moves = 0

            while moves < self.MOVES_PER_GAME:
                # choose A according to a policy
                action = self.decreasing_e_greedy(i, self.INITIAL_EPSILON)
                if action is None:
                    break

                # take action A and observe R
                reward = self.game.make_move(action)
                total_score += reward


                # observe S'
                s_prime = self.get_features()

                # Update weights
                q_s_prime = sum([s_prime[i] * self.weights[i] for i in range(len(s_prime))])
                q_s = sum([self.feature_vector[i] * self.weights[i] for i in range(len(self.feature_vector))])
                for i in range(len(self.weights)):
                    self.weights[i] = self.weights[i] + self.ALPHA * (reward + self.GAMMA * q_s_prime - q_s) * self.feature_vector[i]

                # Update S and check for termination
                self.feature_vector = s_prime

                if self.game.checkIfCompleted():
                    won = True
                    break
                moves += 1

            #Update score and wins/losses list based off of win/loss
            if won:
                total_score += 1000
                wins.append(1)
                print("WON THIS GAME")
            else:
                total_score -= 100
                wins.append(0)

            total_moves.append(moves)
            final_scores.append(total_score)
            print(self.game.getGameElements())



        return total_moves, final_scores, wins

    # helper methods, etc

    # update feature vector
    # DO NOT update first value- always keep at 1
    def get_features(self, thisGame=None):
        # this method should return a feature vector according to the game elements "printout" received from self.game or the specified game
        return_vector = [1]
        if thisGame:
            for pile in thisGame.blockPiles.values():
                return_vector.append(len(pile.cards))

                # get number of flipped cards in each play pile and update
            for pile in thisGame.playPiles:
                return_vector.append(len(pile.getFlippedCards()))

        else:

            for pile in self.game.blockPiles.values():
                return_vector.append(len(pile.cards))

            # get number of flipped cards in each play pile and update
            for pile in self.game.playPiles:
                return_vector.append(len(pile.getFlippedCards()))

        return return_vector

LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1
NUM_TRAINING_GAMES = 1000
MOVE_LIMIT = 1000

agent = QLearningAgent(EPSILON, DISCOUNT_FACTOR, LEARNING_RATE, MOVE_LIMIT, NUM_TRAINING_GAMES)

total_moves, final_scores, wins = agent.learn()

print(total_moves)
print(final_scores)
print(wins)



#TODO: use total move and final score data to do some graphing / analysis
