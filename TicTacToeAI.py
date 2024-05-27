import random
import copy

BOARD_WIDTH = 3
BOARD_HEIGHT = 3
PLAYER_1 = "X"
PLAYER_2 = "O"
#MAX_SCORE = 10
MAX_GAMES = 6

#takes nothing
#returns list of lists of size BOARD_WIDTH, BOARD_HEIGHT
def new_board(old_board=None, move=None, player=None):

    if old_board == None:
        board = []
        for x in range(0, BOARD_WIDTH):
            column = []
            for y in range(0, BOARD_HEIGHT):
                column.append(None)
            board.append(column)
    else:
        board = old_board

    if move!=None and player != None:
        board[move[0]-1][move[1]-1] = player


    return board


#takes a list of lists size 3,3
#prints board to console
def print_board(board):
    print("  1   2   3")
    for y in range(0, len(board)):
        line = str(y+1)+" "
        for x in range(0, len(board[0])):
            line += (board[x][y] if board[x][y]!=None else " ")
            if x != len(board[0])-1:
                line+=" | "
        print(line)
        if y != len(board)-1:
            print("  ---------")

#takes a player symbol
#returns move given by player, using a list of ints of size 2
def get_move_human(board, player):
    str = input(player+"'s turn. Enter coordinates of your move(x,y): ")
    list = str.split()
    error = None
    if len(list)!=2:
        return error, "Wrong number of coordinates. Must be 2"

    for i in range(0,len(list)):
        try:
            list[i] = int(list[i])
        except ValueError:
            return error, "Coordinates must be 2 integers in [1,3] seperated with a space"
        

    if not ((1 <= list[0] <= 3) and (1 <= list[1] <= 3)):
        return error, "Coordinate is out of bounds. [1,3]"


    return list,None

#takes move(list of coordinates), board, and player symbol
#returns a new board with move added
def make_move(move, board, player):

    b = new_board(board, move, player)

    return b

#takes board and move(list of coordinates)
#returns boolean, and reason if boolean is false
def is_valid_move(board, move):
    if not isinstance(move, list):
        return False, "not list"
    if not len(move) == 2:
        return False, "length != 2"
    if type(move[0]) != int or type(move[1])!=int:
        return False, "are not ints"
    if not ((1 <= move[0] <= 3) and (1 <= move[1] <= 3)):
        return False, "out of bounds"
    if board[move[0]-1][move[1]-1] != None:
        return False, "space already occupied"
    return True, None

#takes board
#returns boolean
def check_tie(board):
    for column in board:
        for space in column:
            if space == None:
                return False
    return True

#takes board
#returns player symbol if there's a winner or None otherwise
def check_win(board):
    all_line_coords = get_all_line_coords()

    for line in all_line_coords:
        line_values = [board[x][y] for (x, y) in line]
        if len(set(line_values)) == 1 and line_values[0] is not None:
            return line_values[0]

    return None

#takes nothing
#returns list of lists that has every way to win
def get_all_line_coords():
    cols = []
    for x in range(0, BOARD_WIDTH):
        col = []
        for y in range(0, BOARD_HEIGHT):
            col.append((x, y))
        cols.append(col)

    rows = []
    for y in range(0, BOARD_HEIGHT):
        row = []
        for x in range(0, BOARD_WIDTH):
            row.append((x, y))
        rows.append(row)

    diagonals = [[],[]]
    for x in range(0, min([BOARD_WIDTH,BOARD_HEIGHT])):
        diagonals[0].append((x,x))
        diagonals[1].append((x,min([BOARD_WIDTH,BOARD_HEIGHT])-x-1))

    return cols + rows + diagonals

#takes nothing
#resets board, returns player going first
#player symbol stays with the player, this changes which symbol goes first
def reset():
    global PLAYER_1, PLAYER_2, p1_get_func, p2_get_func
    temp = PLAYER_1
    PLAYER_1 = PLAYER_2
    PLAYER_2 = temp

    temp = p1_get_func
    p1_get_func = p2_get_func
    p2_get_func = temp
    return new_board(), PLAYER_1

#takes board
#returns list of coordinates of empty spaces
def get_empty(board):
    empty = []

    for y in range(0, len(board)):
        for x in range(0, len(board[0])):
            if board[x][y] == None:
                empty.append([x+1,y+1])
    return empty

#takes player symbol
#returns other player symbol
def get_opposite(player):
    if player == "X":
        return "O"
    elif player == "O":
        return "X"
    else:
        return None

#takes a board and player symbol
#returns move given by random ai, using a list of ints of size 2
def get_move_random(board, player):
    empty = get_empty(board)

    if len(empty)==0:
        return None, "No spaces left"

    index = random.randrange(0,len(empty))
    print(empty[index])

    return empty[index], ""

#takes board and player symbol
#returns move given by perfect ai(list of coordinates)
def get_move_perfect(board, player):
    print("Perfect AI is thinking...")
    best_move = None
    best_score = None
    empties = get_empty(board)
    
    if len(empties) == 9:#speed optimization for going 1st
        return [1,1], ""

    for move in empties:
        _board = copy.deepcopy(board)
        make_move(move, _board, player)

        opp = get_opposite(player)
        score = _minimax_score(_board, opp, player)
        if best_score is None or score > best_score:
            best_move = move
            best_score = score

    return best_move, ""

#takes board, player symbol, player symbol
#returns score
def _minimax_score(board, player_to_move, player_to_optimize):
    #if there is a winner return max score
    winner = check_win(board)
    if winner is not None:
        if winner == player_to_optimize:
            return 10
        else:
            return -10
    elif check_tie(board):
        return 0

    #get all legal moves
    legal_moves = get_empty(board)

    #for each legal move find the one with the most wins(or least)
    scores = []
    for move in legal_moves:
        _board = copy.deepcopy(board)
        make_move(move, _board, player_to_move)

        opp = get_opposite(player_to_move)
        opp_best_response_score = _minimax_score(_board, opp, player_to_optimize)
        scores.append(opp_best_response_score)

    if player_to_move == player_to_optimize:
        return max(scores)
    else:
        return min(scores)

#takes board and current player symbol
#returns simple move
def get_move_simple(board,player):
    print("Simple AI is thinking...")
    moves = get_empty(board)
    if len(moves)==0:#error checking
        return None, "No possible moves"
    elif len(moves)==1:#speed optimization
        print("Simple: last move")
        return moves[0], ""
    elif len(moves)==9:#speed optimization
        print("Simple: random move 1")
        return moves[random.randrange(0,len(moves))], ""

    opp = get_opposite(player)
    for move in moves:
        _board = copy.deepcopy(board)
        _board = make_move(move,_board,player)

        win = check_win(_board)
        #if move result in winning, use it
        if win == player:
            print("Simple: win move")
            return move, ""

        #otherwise check counter moves for opponent
        opp_moves = get_empty(_board)
        for opp_move in opp_moves:
            __board = copy.deepcopy(_board)
            __board = make_move(opp_move,__board,opp)

            opp_win = check_win(__board)
            #if move results in opponent winning, block move
            if opp_win==opp:
                print("Simple: block move")
                return opp_move, ""

    print("Simple: random move 2")
    return moves[random.randrange(0,len(moves))], ""

#create new board and print it
board = new_board()
print()
print_board(board)

#set up game control variables
player = PLAYER_1#current player symbol
#--------------------------------------------------------------------------------------------------------------------
#options are:
#               get_move_perfect
#               get_move_human
#               get_move_simple
#               get_move_random
p1_get_func = get_move_simple   #first get move function
p2_get_func = get_move_human    #second get move function
#--------------------------------------------------------------------------------------------------------------------
scores = {"X":0,"O":0}#number of games won(doesn't count ties)
games = 0#number of games played
print("Playing "+str(MAX_GAMES)+" games.")

#loop until max number of games is reached
while True:
    #get move
    if player == PLAYER_1:
        move,why = p1_get_func(board, player)
    else:
        move,why = p2_get_func(board, player)

    if move == None:
        print(why)
    else:
        #make sure mvoe is valid
        result, why = is_valid_move(board, move)
        if result:
            #add move to board
            board = make_move(move, board, player)
            print_board(board)
            #check for a winner
            if check_win(board):
                print(player+" won the set!")
                scores[player] += 1
                games += 1
                if games >= MAX_GAMES:
                    print(str(scores[PLAYER_1])+" to "+str(scores[PLAYER_2]))
                    break
                else:
                    print("Games finished: "+str(games))
                #reset board and switch players
                board,player = reset()
                print()
                print_board(board)
                continue
            #check for tie
            if check_tie(board):
                print("It's a tie.")
                games += 1
                if games >= MAX_GAMES:
                    print(str(scores[PLAYER_1])+" to "+str(scores[PLAYER_2]))
                    break
                else:
                    print("Games finished: "+str(games))
                #reset board and switch players
                board,player = reset()
                print()
                print_board(board)
                print()
                continue
            #change current player symbol
            if player == PLAYER_1:
                player = PLAYER_2
            else:
                player = PLAYER_1
        else:
            print("Invalid move: "+why)
