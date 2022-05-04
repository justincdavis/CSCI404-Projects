import os
import sys
import numpy as np
import copy
from typing import List


# EXTRA CREDIT NOTE
# this defines all moves in a defined way from left to right from a given starting position.
# since minimax iterates over the postions of these in order, there is an inorder traversal of the game tree.
# thus this implements successor node priorization since that specifies the traversal is in order.
def getChildPositions(position, maxplayer=True, currentPlayer=None):
    possible_child = []
    value = 1 if maxplayer else 2
    if currentPlayer is not None:
        value = currentPlayer
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


def evalGame(position, maxplayer=True, raw=False):
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

    if raw:
        return p1Score, p2Score

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


def getNextGameState(position, current_player, depth=50, maxplayer=True):
    best_position = None
    best_eval = -np.inf
    for child in getChildPositions(position, maxplayer, currentPlayer=current_player):
        childEval = minimax(child, maxplayer=maxplayer, depth=depth)
        if childEval >= best_eval:
            best_position = child
    player_return = 1 if current_player == 2 else 2
    return best_position, player_return


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
    return start_grid, player


def writeOutput(current_position, current_player, filename="output.txt", write=True, print_game=False):
    position = copy.deepcopy(current_position)
    for col in position:
        col.reverse()
    output_lines = []
    for row in zip(*tuple(position)):
        output_str = ""
        for value in row:
            output_str += str(value)
        output_str += '\n'
        output_lines.append(output_str)
    output_lines.append(current_player)
    if write:
        with open(filename, 'w') as f:
            for line in output_lines:
                try:
                    f.write(line)
                except TypeError:
                    f.write(str(line))
    if print_game:
        for line in output_lines:
            try:
                line = line.strip()
                line = line.split()
                output_line = ""
                for idx, char in enumerate(line):
                    output_line += char
                    if idx != len(line) - 1:
                        output_line += ", "
                print(output_line)
            except AttributeError:
                print(f"Current player: {current_player}")


def printGameBoard(current_position: List[List[int]], current_player):
    writeOutput(current_position, current_player, ".", write=False, print_game=True)


def printGame(position: List[List[int]], startNum):
    print("================================================")
    print("CURRENT GAME STATE")
    printGameBoard(position, startNum)
    scores = evalGame(position, raw=True)
    print(f"Player 1: {scores[0]}, Player 2: {scores[1]}")
    print("================================================")


def checkValidCol(position, col):
    for col_idx, column in enumerate(position):
        if col_idx == col - 1:
            for spot in column:
                if spot == 0:
                    return True
    return False


def placePieceInColumn(position, column, currentPlayer):
    for col_idx, col in enumerate(position):
        if col_idx == column - 1:
            for idx, space in enumerate(col):
                if space == 0:
                    col[idx] = currentPlayer
                    return position


def humanGetColumn(position):
    while True:
        try:
            col = int(input("Please select which column you would like to place your piece in (from 1 to 7)"))
            if checkValidCol(position, col):
                return col
        except ValueError:
            pass
        finally:
            if not isGameOver(position):
                print("Invalid column entry!")


def interactive(position: List[List[int]], currentPlayer: int, humanNext: bool, depth: int):
    first_move = True
    printGame(position, currentPlayer)
    while not isGameOver(position):
        if not humanNext:
            if not first_move:
                position, currentPlayer = readInput("human.txt")
                printGame(position, currentPlayer)
            else:
                first_move = False
            position, currentPlayer = getNextGameState(position, currentPlayer, depth=depth)
            writeOutput(position, currentPlayer, filename="computer.txt")
            humanNext = not humanNext
        else:
            if not first_move:
                position, currentPlayer = readInput("computer.txt")
                printGame(position, currentPlayer)
            else:
                first_move = False
            column = humanGetColumn(position)
            position = placePieceInColumn(position, column, currentPlayer)
            if currentPlayer == 1:
                currentPlayer = 2
            else:
                currentPlayer = 1
            writeOutput(position, currentPlayer, filename="human.txt")
            humanNext = not humanNext
    if not first_move:
        printGame(position, currentPlayer)
    print("Game is over, exiting...")
    return


def oneMove(position: List[List[int]], startNum: int, outputFile: str, depth: int):
    printGame(position, startNum)
    if isGameOver(position):
        print("Game is over, exiting...")
        return
    new_position, currentPlayer = getNextGameState(position, startNum, depth=depth)
    printGame(new_position, currentPlayer)
    writeOutput(new_position, currentPlayer, outputFile)


if __name__ == "__main__":
    modes = ["interactive", "one-move"]
    args = sys.argv[1:len(sys.argv)]

    assert len(args) == 4, "Did not supply sufficient arguments"

    # check to ensure we have a good mode
    mode = args[0].strip()
    assert mode in modes, f"{mode} is not a valid mode, Mode: {modes}"
    # check to ensure the input file exists
    input_file = args[1].strip()
    assert os.path.exists(input_file), f"{input_file} does not exist"
    # check to ensure depth is greater than 0
    start_depth = int(args[3])
    assert start_depth > 0, "Depth needs to be greater than 0!"

    starting_game, starting_num = readInput(input_file)

    if mode == "interactive":
        # check to ensure the next player flag is valid
        players = ["computer-next", "human-next"]
        next_player = args[2].strip()
        assert next_player in players, f"{next_player} is not a valid player, valid options are: {players}"

        player_flag = True if next_player == "human-next" else False

        interactive(starting_game, starting_num, player_flag, start_depth)

    elif mode == "one-move":
        output_file = args[2].strip()
        oneMove(starting_game, starting_num, output_file, start_depth)
