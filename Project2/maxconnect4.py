import os
import sys
import numpy as np
import copy


def getChildPositions(position, maxplayer):
    possible_child = []
    value = 1 if maxplayer else 2
    for col_idx, column in enumerate(position):
        child_position = copy.deepcopy(position)
        for row_idx, space in enumerate(column):
            if space == 0:
                child_position[col_idx][row_idx] = value
                possible_child.append(child_position)
                break
    return possible_child


def _evalDiag(group):
    if group.count(group[0]) == 4 and group[0] != 0:
        if group[0] == 1:
            return 1, 0
        elif group[0] == 2:
            return 0, 1
    return 0, 0


def _evalRowCol(rc):
    p1Score = 0
    p2Score = 0
    for i in range(0, len(rc) - 3):
        if rc[i:i + 4].count(rc[i]) == 4 and rc[i] != 0:
            if rc[i] == 1:
                p1Score += 1
            elif rc[i] == 2:
                p2Score += 1
    return p1Score, p2Score


def _updateScores(p1Score, p2Score, p1Add, p2Add):
    return p1Score + p1Add, p2Score + p2Add


def evalGame(position, maxplayer):
    p1Score = 0
    p2Score = 0

    # checks a score on each row
    for row in zip(*tuple(position)):
        p1Add, p2Add = _evalRowCol(row)
        p1Score, p2Score = _updateScores(p1Score, p2Score, p1Add, p2Add)

    # checks a score on each col
    for col in (tuple(position)):
        p1Add, p2Add = _evalRowCol(col)
        p1Score, p2Score = _updateScores(p1Score, p2Score, p1Add, p2Add)

    # checks a score on each diagonal
    # down right: col_idx, row_idx; col_idx+1, row_idx-1; col_idx+2, row_idx-2; col_idx+3, row_idx-3
    # up right: col_idx, row_idx; col_idx+1, row_idx+1; col_idx+2, row_idx+2; col_idx+3, row_idx+3
    # down left: col_idx, row_idx; col_idx-1, row_idx-1; col_idx-2, row_idx-2; col_idx-3, row_idx-3
    # up left: col_idx, row_idx; col_idx-1, row_idx+1; col_idx-2, row_idx+2; col_idx-3, row_idx+3
    for c in range(len(position)):
        for r in range(len(position[0])):
            if r >= 3 and c <= len(position) - 4:
                dr = (position[c][r], position[c+1][r-1], position[c+2][r-2], position[c+3][r-3])
                p1Add, p2Add = _evalDiag(dr)
                p1Score, p2Score = _updateScores(p1Score, p2Score, p1Add, p2Add)
            if r <= len(position[0]) - 4 and c <= len(position) - 4:
                ur = (position[c][r], position[c+1][r+1], position[c+2][r+2], position[c+3][r+3])
                p1Add, p2Add = _evalDiag(ur)
                p1Score, p2Score = _updateScores(p1Score, p2Score, p1Add, p2Add)
            if r >= 3 and c >= 3:
                dl = (position[c][r], position[c-1][r-1], position[c-2][r-2], position[c-3][r-3])
                p1Add, p2Add = _evalDiag(dl)
                p1Score, p2Score = _updateScores(p1Score, p2Score, p1Add, p2Add)
            if r <= len(position[0]) - 4 and c >= 3:
                ul = (position[c][r], position[c-1][r+1], position[c-2][r+2], position[c-3][r+3])
                p1Add, p2Add = _evalDiag(ul)
                p1Score, p2Score = _updateScores(p1Score, p2Score, p1Add, p2Add)

    if maxplayer:
        return p1Score - p2Score
    else:
        return p2Score - p1Score


def isGameOver(position):
    found_empty = False
    for column in position:
        for space in column:
            if space == 0:
                found_empty = True
    return not found_empty


def minimax(position, depth=50, alpha=np.inf, beta=-np.inf, maxplayer=True):
    if depth == 0 or isGameOver(position):
        return evalGame(position, maxplayer)

    if maxplayer:
        maxEval = -np.inf
        for child in getChildPositions(position, maxplayer):
            new_eval = minimax(child, depth=depth-1, alpha=alpha, beta=beta, maxplayer=False)
            maxEval = max(maxEval, new_eval)
            alpha = max(alpha, new_eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = np.inf
        for child in getChildPositions(position, maxplayer):
            new_eval = minimax(child, depth=depth-1, alpha=alpha, beta=beta, maxplayer=True)
            minEval = min(minEval, new_eval)
            beta = min(beta, new_eval)
            if beta <= alpha:
                break
        return minEval


# TODO
# write action chooser function. Given the output of minimax, find a gamestate from getChildPositions which has the
# same score. Can just return the first one


def readInput(filename):
    start_grid = [[0] * 6 for i in range(7)]
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [list(line.strip()) for line in lines]  # strips newlines from all strings
    lines = [[int(value) for value in line] for line in lines]
    lines, player = lines[:-1], lines[len(lines)-1][0]
    for row_idx, line in enumerate(lines):
        for col_idx, value in enumerate(line):
            start_grid[col_idx][row_idx] = value
    for col in start_grid:
        col.reverse()
    return start_grid, True if player == 1 else False


def writeOutput(position, maxplayer, filename="output.txt"):
    for col in position:
        col.reverse()
    output_lines = []
    for row in zip(*tuple(position)):
        output_str = ""
        for value in row:
            output_str += str(value)
        output_lines.append(output_str)
    output_lines.append(str(1 if maxplayer else 2))
    with open(filename, 'w') as f:
        for line in output_lines:
            f.write(line)


if __name__ == "__main__":
    grid, starting_player = readInput('input3.txt')

    num = minimax(grid, maxplayer=starting_player)

    print(num)
