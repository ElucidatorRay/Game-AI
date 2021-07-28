import numpy as np
import math
import copy


def SomeoneWin(game):
    # 判斷橫的
    for i in range(3):
        if (game[i] == -1).all():
            return -1
        if (game[i] == 1).all():
            return 1
    # 判斷綜的
    for j in range(3):
        L = []
        for i in range(3):
            L.append(game[i][j])
        if (np.array(L) == -1).all():
            return -1
        if (np.array(L) == 1).all():
            return 1
    # 判斷斜的
    L = [game[0][0], game[1][1], game[2][2]]
    if (np.array(L) == -1).all():
        return -1
    if (np.array(L) == 1).all():
        return 1
    L = [game[2][0], game[1][1], game[0][2]]
    if (np.array(L) == -1).all():
        return -1
    if (np.array(L) == 1).all():
        return 1
    return 0


def getScore(game, WHO):
    '''計算當前局面的分數'''
    score = 0
    # 考慮橫向
    for i in range(3):
        L = list(game[i])
        # 如果占據兩格，而且第三格為空
        if L.count(WHO) == 2 and L.count(0) == 1:
            score += 2
        # 如果佔據1格，而且其餘兩格為空
        elif L.count(WHO) == 1 and L.count(0) == 2:
            score += 1
        # 如果佔據三格
        elif L.count(WHO) == 3:
            score += 10000
        else:
            continue
    # 考慮縱向
    for i in range(3):
        L = [game[0][i], game[1][i], game[2][i]]
        # 如果占據兩格，而且第三格為空
        if L.count(WHO) == 2 and L.count(0) == 1:
            score += 2
        # 如果佔據1格，而且其餘兩格為空
        elif L.count(WHO) == 1 and L.count(0) == 2:
            score += 1
        # 如果佔據三格
        elif L.count(WHO) == 3:
            score += 10000
        else:
            continue
    # 考慮斜項
    L = [game[0][0], game[1][1], game[2][2]]
    if L.count(WHO) == 2 and L.count(0) == 1:
        score += 2
    elif L.count(WHO) == 1 and L.count(0) == 2:
        score += 1
    # 如果佔據三格
    elif L.count(WHO) == 3:
        score += 10000
    else:
        pass
    L = [game[2][0], game[1][1], game[0][2]]
    if L.count(WHO) == 2 and L.count(0) == 1:
        score += 2
    elif L.count(WHO) == 1 and L.count(0) == 2:
        score += 1
    # 如果佔據三格
    elif L.count(WHO) == 3:
        score += 10000
    else:
        pass
    return score


def show(game):
    D = {1: 'O', -1: 'X', 0: ' '}
    print('---------')
    print('| ' + f'{D[game[0][0]]}' + ' ' +
          f'{D[game[0][1]]}' + ' ' + f'{D[game[0][2]]}' + ' |')
    print('| ' + f'{D[game[1][0]]}' + ' ' +
          f'{D[game[1][1]]}' + ' ' + f'{D[game[1][2]]}' + ' |')
    print('| ' + f'{D[game[2][0]]}' + ' ' +
          f'{D[game[2][1]]}' + ' ' + f'{D[game[2][2]]}' + ' |')
    print('---------')


class Node():
    def __init__(self, game, level):
        self.data = game
        self.score = (getScore(game, -1) - getScore(game, 1))
        self.childs = []
        self.scores = []
        self.level = level
    def print_childs(self):
        for child in self.childs:
            show(child.data)


def build_tree(game, level, WHO):
    root = Node(game, level)
    if level == 1 or 0 not in game or SomeoneWin(game):
        return root
    else:
        for i in range(3):
            for j in range(3):
                if game[i][j] != 0:
                    continue
                subgame = copy.deepcopy(game)
                subgame[i][j] = WHO
                newtree = build_tree(subgame, level-1, WHO*-1)
                root.childs.append(newtree)
                root.scores.append(newtree.score)
        return root


def get_node_number(root):
    SUM = 0
    for elem in root.childs:
        SUM += get_node_number(elem)
    return 1 + SUM


def get_move(before, after):
    diff = after - before
    X = int(np.where(diff[diff != 0] == diff)[0])
    Y = int(np.where(diff[diff != 0] == diff)[1])
    return (X, Y)

    
def find_max(root):
    MAX = -2**100
    move = None
    for i in range(len(root.childs)):
        if root.scores[i] + find_min(root.childs[i])[0] > MAX:
            MAX = root.scores[i] + find_min(root.childs[i])[0]
            move = get_move(root.data, root.childs[i].data)
    if MAX == -2**100:
        MAX = 0
    return MAX, move

            
def find_min(root):
    MIN = 2**100
    move = None
    for i in range(len(root.childs)):
        if root.scores[i] + find_max(root.childs[i])[0] < MIN:
            MIN = root.scores[i] + find_max(root.childs[i])[0]
            move = get_move(root.data, root.childs[i].data)
    if MIN == 2**100:
        MIN = 0
    return MIN, move