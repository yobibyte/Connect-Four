from minimax import Minimax
import nn
import random
from game_util import check_streaks
import numpy as np

MEM_SIZE = 100
BATCH_SIZE = 32
EPS = 0.1

class Player(object):
    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color
        self.g = g

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column

class AIPlayer(Player):
    """ AIPlayer object that extends Player
        The AI algorithm is minimax, the difficulty parameter is the depth to which
        the search tree is expanded.
    """

    difficulty = None
    def __init__(self, name, color, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.ctr = 0

    def move(self, state):
        print("{0}'s turn.  {0} is {1}, {2}".format(self.name, self.color, self.ctr))
        self.ctr+=1
        m = Minimax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        return best_move

class DQNPlayer(Player):
    """ DQNPlayer object that extends Player
        Here I use DQN algorithm from Barton&Sutton book + DeepMind atari paper
    """

    difficulty = None
    def __init__(self, name, color, g):
        self.type = "AI"
        self.name = name
        self.color = color
        self.ctr = 0
        self.g = g
        self.replay_memory = [0 for i in range(MEM_SIZE)]
        self.reward = 0
        self.model = nn.create_model()
        try:
            self.model.load_weights('my_model_weights.h5')
        except:
            pass

    def phi(self, ctr, state=None):
        res = np.array([
            self.replay_memory[ctr-3][0],
            self.replay_memory[ctr-2][0],
            self.replay_memory[ctr-1][0],
            self.replay_memory[ctr]
        ])
        if state:
            res[-1] = state
        return res

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))

        legal_moves = [i for i in range(7) if state[-1][i] == 0 ]
        print(legal_moves)
        if random.random() < EPS or self.ctr < MEM_SIZE:
            best_move = random.choice(legal_moves)
        else:
            pred = model.predict(phi(self.ctr, state), batch_size = 1)
            pred = [m for m in pred if m in legal_moves]
            best_move = np.argmax(pred)
            tmp_board = self.makeMove(state, best_move, self.color)
            if check_streaks(tmp_board, 4):
                self.reward += 1
            s_tp1 = state.copy()
            s_tp1[best_move] = self.color
            self.replay_memory[self.ctr % MEM_SIZE - 1] = (state, best_move, self.reward, s_tp1)
            curr_batch = random.sample(range(3, MEM_SIZE), BATCH_SIZE)
            x_j = [self.phi(i) for i in curr_batch]
            #TODO add terminal check for y_j
            y_j = np.array([self.model.predict(np.array([el]), batch_size=1)[0] for el in x_j])
            self.model.fit(x_j, y_j, nb_epoch=1, verbose=0, batch_size=32)
        return best_move

    def save_model():
        self.model.save_weights('dqn_model.h5')

    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            Returns a copy of new state array with the added move
        """
        temp = state.copy()
        for i in range(6):
            if temp[i][column] == 0:
                temp[i][column] = color
                return temp
