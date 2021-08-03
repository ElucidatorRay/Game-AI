import pygame
import random
import numpy as np

class Grid():
    GridSize = 75
    STABLE = 1
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.state = 0
        self.stable = 0

    def SetState(self, newState):
        self.state = newState
    
    def SetStable(self):
        self.stable = Grid.STABLE

class Reversi():
    STABLE = 1
    MOVE = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    def __init__(self):
        self.game = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(Grid(i, j))
            self.game.append(row)
        self.game[3][4].SetState(-1)
        self.game[4][3].SetState(-1)
        self.game[3][3].SetState(1)
        self.game[4][4].SetState(1)
    
    def getStateMap(self):
        StateMap = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(self.game[i][j].state)
            StateMap.append(row)
        return StateMap

    def getStableMap(self):
        StableMap = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(self.game[i][j].stable)
            StableMap.append(row)
        return StableMap

    def getValidPosi(self, currentPlayer):
        ValidMoveList = []
        for i in range(8):
            for j in range(8):
                if self.game[i][j].state == 1 or self.game[i][j].state  == -1:
                    continue
                else:
                    self.game[i][j].SetState(0)
                for move in Reversi.MOVE:
                    find = False
                    ChangeNo = 0
                    newi, newj = i + move[0], j + move[1]
                    while not (newi < 0 or newi >= 8 or newj < 0 or newj >= 8):
                        if self.game[newi][newj].state == -1*currentPlayer:
                            ChangeNo += 1
                            newi, newj = newi + move[0], newj + move[1]
                            continue
                        elif self.game[newi][newj].state == currentPlayer:
                            if ChangeNo != 0:
                                ValidMoveList.append((i, j))
                            find = True
                            break
                        else:
                            find = True
                            break
                    if find:
                        continue
        return ValidMoveList

    def UpdateGameState(self, X, Y, newState):
        self.game[X][Y].SetState(newState)
        for move in Reversi.MOVE:
            ChangeList = []
            newX, newY = X + move[0], Y + move[1]
            while not (newX < 0 or newX >= 8 or newY < 0 or newY >= 8):
                if self.game[newX][newY].state == -1*newState:
                    ChangeList.append((newX, newY))
                    newX, newY = newX + move[0], newY + move[1]
                    continue
                if self.game[newX][newY].state == newState:
                    for change in ChangeList:
                        self.game[change[0]][change[1]].SetState(newState)
                    break
                if self.game[newX][newY].state not in (newState, -1*newState):
                    break

    def isValidGrid(self, X, Y):
        if X < 0 or X >= 8:
            return False
        if Y < 0 or Y >= 8:
            return False
        return True

    def isStableGrid(self, X, Y):
        ThisPlayer = self.game[X][Y].state
        if ThisPlayer not in (-1, 1):
            return False
        # 考慮縱向
        left = ( (X-1) < 0 or (self.game[X-1][Y].stable == 1 and self.game[X-1][Y].state == ThisPlayer) )
        right = ( (X+1) > 7 or (self.game[X+1][Y].stable == 1 and self.game[X+1][Y].state == ThisPlayer) )
        if not (left or right):
            return False
        # 考慮橫向
        up = ( (Y-1) < 0 or (self.game[X][Y-1].stable == 1 and self.game[X][Y-1].state == ThisPlayer) )
        down = ( (Y+1) > 7 or (self.game[X][Y+1].stable == 1 and self.game[X][Y+1].state == ThisPlayer) )
        if not (up or down):
            return False
        # 考慮左上右下斜向
        leftup = ( ((X-1) < 0 or (Y-1) < 0) or (self.game[X-1][Y-1].stable == 1 and self.game[X-1][Y-1].state == ThisPlayer) )
        rightdown = ( ((X+1) > 7 or (Y+1) > 7) or (self.game[X+1][Y+1].stable == 1 and self.game[X+1][Y+1].state == ThisPlayer) )
        if not (leftup or rightdown):
            return False 
        # 考慮右上左下斜向
        leftdown = ( ((X-1) < 0 or (Y+1) > 7) or (self.game[X-1][Y+1].stable == 1 and self.game[X-1][Y+1].state == ThisPlayer) )
        rightup = ( ((X+1) > 7 or (Y-1) < 0) or (self.game[X+1][Y-1].stable == 1 and self.game[X+1][Y-1].state == ThisPlayer) )
        if not (leftdown or rightup):
            return False
        return True

    def UpdateGameStable(self):
        hasStable = False
        for posi in ((0, 0), (7, 7), (0, 7), (7, 0)):
            if self.game[posi[0]][posi[1]].state in (-1, 1):
                self.game[posi[0]][posi[1]].stable = 1
                hasStable = True
        if hasStable:
            while True:
                previous = self.getStableMap()
                for i in range(8):
                    for j in range(8):
                        if self.isStableGrid(i, j):
                            # print(i, '  ', j)
                            self.game[i][j].stable = 1
                            # return
                if previous == self.getStableMap():
                    break

    def getCurrentScore(self):
        White, Black = 0, 0
        for i in range(8):
            for j in range(8):
                if self.game[i][j].state == 1:
                    White += 1
                elif self.game[i][j].state == -1:
                    Black += 1
        return (White, Black)

    def isFinish(self):
        for row in self.getStateMap():
            for state in row:
                if state == 0.5 or state == -0.5:
                    return False
        return True

def getGridLines():
    Width = 5
    GridLines = []
    for posi in range(0, 601, 75):
        GridLines.append(pygame.Rect(posi - Width/2, 0, Width, 600))
        GridLines.append(pygame.Rect(0, posi - Width/2, 600, Width))
    return GridLines

def getClickPosi(posi):
    Y, X = posi[0]//75, posi[1]//75
    if X < 0 or X >= 8:
        return (-1, -1)
    if Y < 0 or Y >= 8:
        return (-1, -1)
    return Y, X



def plotSceneRect(screen, counter):
    Width = 5
    # board 
    pygame.draw.rect(screen, (0, 158, 11), pygame.Rect(350, 150, 300, 300))
    # vertical grid line
    for posi in range(350, 651, 75):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(posi - Width/2, 150, Width, 300))
    # horizontal line
    for posi in range(150, 451, 75):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(350, posi - Width/2, 300, Width))
    # pieces
    piece = np.array(
    [[[0., 0., 0., 0.],
      [0., +1, -1, 0.],
      [0., -1, +1, 0.],
      [0., 0., 0., 0.]],
     [[0., 0., 0., 0.],
      [-1, -1, -1, 0.],
      [0., -1, +1, 0.],
      [0., 0., 0., 0.]],
     [[+1, 0., 0., 0.],
      [-1, +1, -1, 0.],
      [0., -1, +1, 0.],
      [0., 0., 0., 0.]],
     [[+1, 0., 0., 0.],
      [-1, +1, -1, 0.],
      [0., -1, -1, -1],
      [0., 0., 0., 0.]],
     [[+1, 0., 0., 0.],
      [-1, +1, -1, 0.],
      [0., +1, -1, -1],
      [0., +1, 0., 0.]]]
    )
    counter = (counter % 1500) // 300
    for i in range(4):
        for j in range(4):
            posi = (350 + (j*75 + (j+1)*75)//2, 150 + (i*75 + (i+1)*75)//2)
            if piece[counter][i][j] == 1:
                pygame.draw.circle(screen, (255, 255, 255), posi, 30)
            elif piece[counter][i][j] == -1:
                pygame.draw.circle(screen, (0, 0, 0), posi, 30)

