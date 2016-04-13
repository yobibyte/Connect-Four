#taken from https://github.com/erikackermann/Connect-Four

import random, os
from players import AIPlayer, DQNPlayer
import numpy as np
from game_util import check_streaks


DIFFICULTY = 0

class Game(object):

    def __init__(self):
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        self.players = [None, None]
        self.colors = [1, -1] #1 for x, -1 for o
        self.players[0] = AIPlayer('1', self.colors[0], DIFFICULTY+1)
        self.players[1] = DQNPlayer('2', self.colors[1], self)
        #self.players[1] = AIPlayer('2', self.colors[1], DIFFICULTY+1)
        self.newGame()

    def newGame(self):
        self.round = 1
        self.finished = False
        self.winner = None
        self.turn = 0
        self.board = np.zeros((6,7), dtype=np.int)

    def switchTurn(self):
        self.turn = 1 if self.turn == 0 else 0
        self.round += 1

    def nextMove(self):
        player = self.players[self.turn]

        if self.round > 42: # 7*6
            self.finished = True # stalemate
            return

        move = player.move(self.board) #move is the column id

        for i in range(6):
            if self.board[i][move] == 0:
                self.board[i][move] = player.color
                self.switchTurn()
                res = check_streaks(self.board, 4)
                if(len(res) > 0):
                    print(res)
                    self.finished = True
                    if self.players[0].color == self.board[i][move]:
                        self.winner = self.players[0]
                    else:
                        self.winner = self.players[1]
                    self.highlightFour(res)
                self.printState()
                return

        print("Invalid move (column is full)")
        return

    def highlightFour(self, coords):
        for el in coords[0]:
            self.board[el[0]][el[1]] = 42

    def printState(self):
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print(u"{0}!".format("Connect Four"))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                curr = self.board[i][j]
                if curr == 1:
                    k = "x"
                elif curr == -1:
                    k = "o"
                elif curr == 42:
                    k = "Q"
                else:
                    k = " "
                print("| " + k, end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")
