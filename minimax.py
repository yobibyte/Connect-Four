#taken from https://github.com/erikackermann/Connect-Four

import random
import numpy as np
from game_util import streaks, check_streaks

class Minimax(object):
    colors = [1, -1] #1 for x, -1 for o

    def __init__(self, board):
        self.board = board.copy()

    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        opp_player = self.colors[1] if curr_player == self.colors[0] else self.colors[0]

        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(7):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth-1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))

        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever
            called this search

            Returns the alpha value
        """

        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

    def isLegalMove(self, column, state):
        return True if state[5][column] == 0 else False

    def gameIsOver(self, state):
        return True if len(check_streaks(state, 4)) >= 1 else False

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

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 +
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        my_fours = len(check_streaks(state, 4 ,color))
        my_threes = len(check_streaks(state, 3, color))
        my_twos = len(check_streaks(state, 2, color))
        opp_fours = len(check_streaks(state, 4, o_color))
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos
