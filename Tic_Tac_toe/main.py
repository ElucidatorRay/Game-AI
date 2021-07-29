import numpy as np
import math
from Tic_tac_toe import *

game = np.array([[0,0,0],[0,0,0],[0,0,0]])
print('1: Player First \n0: Computer First')
Ans = int(input('Choose: '))
if Ans == 1:
    player_first = True
elif Ans == 0:
    player_first = False

if player_first:
    th = 1
    while SomeoneWin(game) == 0:
        print(f'The {th}-th play')
        show(game)
        while True:
            X = int(input('X: '))
            Y = int(input('Y: '))
            if X in (0, 1, 2) and Y in (0, 1, 2) and game[X][Y] == 0:
                break
        game[X][Y] = 1
        
        if SomeoneWin(game) != 0 or 0 not in game:
            break
        
        root = build_tree(game, 5, -1)
        move = find_max(root)[1]
        print('Move: ',move)
        game[move[0]][move[1]] = -1
        th += 1
    show(game)
    if SomeoneWin(game) == -1:
        print('Comuter win!')
    else:
        print('Player win!')

if not player_first:
    th = 1
    while SomeoneWin(game) == 0:
        print(f'The {th}-th play')
        root = build_tree(game, 5, -1)
        move = find_max(root)[1]
        print('Move: ',move)
        game[move[0]][move[1]] = -1

        if SomeoneWin(game) != 0 or 0 not in game:
            break

        show(game)
        while True:
            X = int(input('X: '))
            Y = int(input('Y: '))
            if X in (0, 1, 2) and Y in (0, 1, 2) and game[X][Y] == 0:
                break
        game[X][Y] = 1
        th += 1
    show(game)
    if SomeoneWin(game) == -1:
        print('Comuter win!')
    else:
        print('Player win!')
