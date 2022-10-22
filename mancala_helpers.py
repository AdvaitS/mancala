
def pad(num: int) -> str:
    return str(num).rjust(2," ") 


def pad_all(nums: list) -> list:
    padded_nums = []
    for num in nums:
        padded_nums.append(pad(num))
    return padded_nums


def initial_state() -> tuple:
    return (0, [4]*8 + [0] + [4]*8 + [0]) 


def game_over(state: tuple) -> bool:
    return all(i == 0 for i in state[1][:8]) or all(j == 0 for j in state[1][9:17]) 

def valid_actions(state: tuple) -> list:
    if state[0] == 0:
        return [i for i in range(8) if state[1][i] != 0]
    else:
        return [i for i in range(9, 17) if state[1][i] != 0] 


def mancala_of(player: int) -> int:
    if player == 0:
        return 8
    else:
        return 17
        

def pits_of(player: int) -> list:
    if player == 0:
        return list(range(8))
    else:
        return list(range(9,17))

def player_who_can_do(move: int) -> int:
    if move in pits_of(0):
        return 0
    else:
        return 1

def opposite_from(position: int) -> int:
    return abs(16-position) 


def play_turn(move: int, board: list) -> tuple:
    new_board = list(board)
    gems = new_board[move]
    new_board[move] = 0
    player = player_who_can_do(move)
    move += 1
    while gems > 1:
        if (move % len(new_board)) == mancala_of(1 - player):
            move += 1
            continue
        new_board[move % len(new_board)] += 1
        gems -= 1
        move += 1
    move, player, gems, new_board = drop_last_gem(move, player, gems, new_board)
    return get_player_turn(move, player, new_board)
    

def clear_pits(board: list) -> list:
    new_board = board
    if len(valid_actions((1, new_board))) == 0:
        for pit in pits_of(0):
            new_board[mancala_of(0)] += new_board[pit]
            new_board[pit] = 0
    else:
        for pit in pits_of(1):
            new_board[mancala_of(1)] += new_board[pit]
            new_board[pit] = 0
    return new_board


def perform_action(action, state):
    player, board = state
    new_player, new_board = play_turn(action, board)
    if 0 in [len(valid_actions((0, new_board))), len(valid_actions((1, new_board)))]:
        new_board = clear_pits(new_board)
    return new_player, new_board

def score_in(state: tuple) -> int:
    player, board = state
    return board[mancala_of(0)] - board[mancala_of(1)] 


def is_tied(board: list) -> bool:
    return score_in((0, board)) == 0 


def winner_of(board: list) -> int:
    if score_in((0, board)) > 0:
        return 0
    else:
        return 1

def get_drop_position(pit, board):
    dummy_board = board
    moves = dummy_board[pit]
    player = player_who_can_do(pit)
    if dummy_board[pit] == 0:
        return pit
    while moves > 0:
        if pit+1%len(dummy_board) == mancala_of(1 - player):
            pit += 1
            continue
        moves -= 1
        pit += 1
    return pit%len(dummy_board)

def get_player_turn(move, player, board):
    if move == mancala_of(player):
        return (player, board)
    else: 
        return (1 - player, board)

def drop_last_gem(move, player, gems, new_board):
    if move in pits_of(player) and new_board[move % len(new_board)] == 0 and new_board[opposite_from(move % len(new_board))] != 0:
        new_board[mancala_of(player)] += gems + new_board[opposite_from(move % len(new_board))]
        new_board[opposite_from(move % len(new_board))] = 0
    elif (move % len(new_board)) == mancala_of(1 - player):
        move += 1
        new_board[move % len(new_board)] += 1
    else:
        new_board[move % len(new_board)] += 1
    return move, player, gems, new_board


def string_of(board: list) -> str:
    opponents_pits = ""
    mancalas = "        "
    players_pits = "          "
    for pit in pits_of(1):
        opponents_pits = " " + pad(board[pit]) + opponents_pits
    opponents_pits = "          " + opponents_pits
    mancalas += pad(board[mancala_of(1)]) + "                         " + pad(board[mancala_of(0)])
    for pit in pits_of(0):
        players_pits += " " + pad(board[pit])
    
    return "\n" + opponents_pits + "\n" + mancalas + "\n" + players_pits + "\n"
