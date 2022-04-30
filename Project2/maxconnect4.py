import os
import sys
import numpy as np


grid = [[0] * 6 for i in range(7)]  # maxPlayer is 1, minPlayer is -1


def getChildPosition(position):
    return [0, 0]


def evalGame(position):
    return 0


def isGameOver(position):
    return False


def minimax(position, depth=18, alpha=np.inf, beta=-np.inf, maxplayer=True):
    if depth == 0 or isGameOver(position):
        return evalGame(position)

    if maxplayer:
        maxEval = -np.inf
        for child in getChildPosition(position):
            new_eval = minimax(child, depth=depth - 1, alpha=alpha, beta=beta, maxplayer=False)
            maxEval = max(maxEval, new_eval)
            alpha = max(alpha, new_eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = np.inf
        for child in getChildPosition(position):
            new_eval = minimax(child, depth=depth - 1, alpha=alpha, beta=beta, maxplayer=True)
            minEval = min(minEval, new_eval)
            beta = min(beta, new_eval)
            if beta <= alpha:
                break
        return minEval
