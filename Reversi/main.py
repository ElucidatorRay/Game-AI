import pygame
import random
import numpy as np
from sys import exit
from utils import *

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Reversi')

NO_infinite = False
clock = pygame.time.Clock()


###############################################################################
font = pygame.font.SysFont("comicsansms", 40)
Title_font = pygame.font.SysFont("comicsansms", 60)
button_font = pygame.font.SysFont("comicsansms", 25)
TITLE = Title_font.render('Reversi', True, (0, 0, 0))
AGAIN = pygame.font.SysFont("comicsansms", 25).render('press R go back to start scene', True, (0,0,0))

while not NO_infinite:
    # assume that players play only one turn
    NO_infinite = True
    start = True
    counter = 0
    while start:
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    start = False
        screen.fill((170, 238, 187))
        plotSceneRect(screen, counter)
        START = button_font.render('press any button to start game', True, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        screen.blit(TITLE,(500 - TITLE.get_width() // 2, 75 - TITLE.get_height() // 2))
        #screen.blit(start_image,(125,150))
        screen.blit(START,(500 - START.get_width() // 2, 525 - START.get_height() // 2))
        pygame.display.flip()
    done = False
    flag1 = False
    flag2 = False
    game = Reversi()
    board, GridLines = pygame.Rect(0, 0, 600, 600), getGridLines()
    currentPlayer = -1
    plot_stable = True
    BLACK = pygame.font.SysFont("comicsansms", 50).render('Black', True, (0, 0, 0))
    WHITE = pygame.font.SysFont("comicsansms", 50).render('White', True, (0, 0, 0))
    ValidMoveList = game.getValidPosi(currentPlayer)
    for posi in ValidMoveList:
        if currentPlayer == 1:
            game.game[posi[0]][posi[1]].SetState(0.5)
        else:
            game.game[posi[0]][posi[1]].SetState(-0.5)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                Y, X = getClickPosi(pygame.mouse.get_pos())
                # 如果點擊位置合法
                if X != -1 and Y != -1 and (X, Y) in ValidMoveList:
                    # 更新state
                    game.UpdateGameState(X, Y, currentPlayer)
                    game.UpdateGameStable()
                    # 判斷對手有無合法落點
                    ValidMoveList = game.getValidPosi(-1*currentPlayer)
                    # 有則更新持棋方，否則繼續由當前玩家操作
                    if len(ValidMoveList) != 0:
                        currentPlayer = currentPlayer*-1
                    else:
                        ValidMoveList = game.getValidPosi(currentPlayer)
                    # 更新可落子位置的state
                    for posi in ValidMoveList:
                        if currentPlayer == 1:
                            game.game[posi[0]][posi[1]].SetState(0.5)
                        else:
                            game.game[posi[0]][posi[1]].SetState(-0.5)
                    # for row1, row2 in zip(game.getStateMap(), game.getStableMap()):
                    #     print(row1, '  ', row2)
                    # print()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_r and flag1 == True:
                    NO_infinite = False
                    flag2 = True
        screen.fill((255, 255, 255))
        # 繪製棋盤、格線、持棋方
        pygame.draw.rect(screen, (0, 158, 11), board)
        for rect in GridLines:
            pygame.draw.rect(screen, (0, 0, 0), rect)
        if currentPlayer == -1:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(602, 0, 200, 75))
        else:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(800, 0, 200, 75))
        screen.blit(BLACK, (700 - BLACK.get_width()//2, 0))
        screen.blit(WHITE, (900 - WHITE.get_width()//2, 0))
        # 繪製stable map
        if plot_stable:
            currentStableMap = game.getStableMap()
            for i in range(8):
                for j in range(8):
                    posi = ( (i*75 + (i+1)*75)//2 , (j*75 + (j+1)*75)//2 )
                    if currentStableMap[j][i] == 1:
                        pygame.draw.circle(screen, (255, 0, 0), posi, 35)
        # 繪製棋子、可行落點
        CurrentSate = game.getStateMap()
        for i in range(8):
            for j in range(8):
                posi = ( (i*75 + (i+1)*75)//2 , (j*75 + (j+1)*75)//2 )
                if CurrentSate[j][i] == 1:
                    pygame.draw.circle(screen, (255, 255, 255), posi, 30)
                elif CurrentSate[j][i] == -1:
                    pygame.draw.circle(screen, (0, 0, 0), posi, 30)
                elif CurrentSate[j][i] == 0.5:
                    pygame.draw.circle(screen, (255, 255, 255), posi, 30, 5)
                elif CurrentSate[j][i] == -0.5:
                    pygame.draw.circle(screen, (0, 0, 0), posi, 30, 5)
        # 判斷遊戲是否結束
        if game.isFinish() and not flag1:
            flag1 = True
            print("Finish")
            WhiteScore, BlackScore = game.getCurrentScore()
            BlackScore = pygame.font.SysFont("comicsansms", 30).render(str(BlackScore), True, (0, 0, 0))
            WhiteScore = pygame.font.SysFont("comicsansms", 30).render(str(WhiteScore), True, (0, 0, 0))
        if flag1:
            screen.blit(AGAIN,(620, 500 - AGAIN.get_height() // 2))
            screen.blit(BlackScore, (700 - BlackScore.get_width()//2, 75))
            screen.blit(WhiteScore, (900 - WhiteScore.get_width()//2, 75))
        if flag2:
            break
        pygame.display.flip()
        clock.tick(60)
pygame.quit()
exit()