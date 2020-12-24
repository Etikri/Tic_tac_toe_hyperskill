def board_print():
    print("---------\n"
          "|", setup[0], setup[1], setup[2], "|\n"
          "|", setup[3], setup[4], setup[5], "|\n"
          "|", setup[6], setup[7], setup[8], "|\n"
          "---------")


#setup = list("_XXOO_OX_")
setup = list("_________")
board_print()
ref = '''
X X X xxx______
_ _ _ ___xxx___
_ _ _ ______xxx

X _ _ x__x__x__
X _ _ _x__x__x_
X _ _ __x__x__x

x _ _ __x_x_x__
_ x _ x___x___x
_ _ x
'''
win_comb = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 1]]


# filter x/0 and covert it to 1/0 form
def board_static_analyze(setup):
    game_status = ""
    filter_x = [1 if x == "X" else 0 for x in setup]
    filter_0 = [1 if x == "O" else 0 for x in setup]
    # if there is nothing on winning position for current winning combination result of subtraction 1, zeroing -1
    # nested list comprehension with [] reverse order, first for x in range(8) then for i in range(9)
    win_pos_minus_current = [[0 if win_comb[x][i] - filter_0[i] <= 0 else 1 for i in range(9)] for x in range(8)]
    # if sum = 0 it means we have winning combination
    win_check_0 = ["O wins" for check in win_pos_minus_current if sum(check) == 0]
    win_pos_minus_current = [[0 if win_comb[x][i] - filter_x[i] <= 0 else 1 for i in range(9)] for x in range(8)]
    win_check_x = ["X wins" for check in win_pos_minus_current if sum(check) == 0]
    # "Impossible" the field has three Xs in a row and three Os in a row.
    if win_check_0 and win_check_x:
        game_status = "Impossible"
    # "Impossible" the field has a lot more Xs that Os or vice versa (if the difference is 2 or more, should be 1 or 0)
    elif abs(sum(filter_x) - sum(filter_0)) > 1:
        game_status = "Impossible"
    # "Draw" no side has a three in a row and there are no empty cells left;
    elif sum(filter_x) + sum(filter_0) == 9 and not (win_check_x or win_check_0):
        game_status = "Draw"
    # "Game not finished" no side has a three in a row and there are still empty cells;
    elif sum(filter_x) + sum(filter_0) < 9 and not (win_check_x or win_check_0):
        game_status = "Game not finished"
    elif win_check_x:
        game_status = win_check_x[0]
    elif win_check_0:
        game_status = win_check_0[0]
    return game_status

# print(game_status)
pos_conv = {"13": 0, "23": 1, "33": 2,
            "12": 3, "22": 4, "32": 5,
            "11": 6, "21": 7, "31": 8}
numbers = "1234567890"
ongoing = True
x_turn = 1
while ongoing:
    game_status = ""
    coords = input("Enter the coordinates: ").replace(" ", "")
    if coords[0] not in numbers or coords[1] not in numbers:
        print("You should enter numbers!")
    elif int(coords[0]) > 3 or int(coords[1]) > 3:
        print("Coordinates should be from 1 to 3!")
    elif setup[pos_conv[coords]] != "_":
        print("This cell is occupied! Choose another one!")
    else:
        if x_turn:
            setup[pos_conv[coords]] = "X"
            board_print()
            filter_x = [1 if x == "X" else 0 for x in setup]
            win_pos_minus_current = [[0 if win_comb[x][i] - filter_x[i] <= 0 else 1 for i in range(9)] for x in range(8)]
            win_check_x = ["X wins" for check in win_pos_minus_current if sum(check) == 0]
            x_turn = 0
            if win_check_x:
                print("X wins")
                break
        elif not x_turn:
            setup[pos_conv[coords]] = "O"
            board_print()
            filter_0 = [1 if x == "O" else 0 for x in setup]
            win_pos_minus_current = [[0 if win_comb[x][i] - filter_0[i] <= 0 else 1 for i in range(9)] for x in range(8)]
            win_check_0 = ["O wins" for check in win_pos_minus_current if sum(check) == 0]
            x_turn = 1
            if win_check_0:
                board_print()
                print("O wins")
                break
        spot_left = [1 for x in setup if x == "_"]
        if not spot_left:
            print("Draw")
            break
