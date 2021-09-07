"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board is initial_state():
        return X
    if terminal(board):
        return None
    
    count = 0
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                count += 1
    if (count % 2 == 0):
        return X
    else:
        return O
       
        
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None
    
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    
    if board_copy[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid Acion!")    
    else:
        board_copy[action[0]][action[1]] = player(board_copy)
    
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check diagonally
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not EMPTY):
        return board[0][2]
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not EMPTY):
        return board[0][0]
    # check horizontally and vertically
    for i in range(3):
        for j in range(3):
            t = 0
            if (board[i][t] == board[i][t+1] == board[i][t+2]) and (board[i][t] is not EMPTY):
                return board[i][t]
            if (board[t][j] == board[t+1][j] == board[t+2][j]) and (board[t][j] is not EMPTY):
                return board[t][j]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    elif winner(board) is O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    optimalMove = None
    # MAX picks action a in ACTIONS(s) that produces highest value(best_v) of MIN-VALUE(RESULT(s, a))
    if player(board) is X:
        best_v = -math.inf
        for action in actions(board):
            max_v = Min_value(result(board, action))
            if max_v > best_v:
                best_v = max_v
                optimalMove = action
    # MIN picks action a in ACTIONS(s) that produces smallest value of MAX-VALUE(RESULT (s, a))
    elif player(board) is O:
        best_v = math.inf
        for action in actions(board):
            min_v = Max_vlaue(result(board, action))
            if min_v < best_v:
                best_v = min_v
                optimalMove = action
    return optimalMove
        
        
def Max_vlaue(board):
    
    if terminal(board):
        return utility(board)
    
    bestScore = -math.inf
    for action in actions(board):
        bestScore = max(bestScore, Min_value(result(board, action)))
    return bestScore
        

def Min_value(board):
    
    if terminal(board):
        return utility(board)
    
    bestScore = math.inf
    for action in actions(board):
        bestScore = min(bestScore, Max_vlaue(result(board, action)))
    return bestScore

