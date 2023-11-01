import numpy as np
import pygame
import sys
# length of row and col 
n=6
m=7
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    board = np.zeros((n,m))
    return board



#graphics
pygame.init()
SQUARE_SIZE = 100
width = SQUARE_SIZE * m 
height = SQUARE_SIZE * n + SQUARE_SIZE
RADIUS = int(SQUARE_SIZE/2 - 2)
size = (width, height)
myfont = pygame.font.Font(None, 59)
textSufaceObj = myfont.render('blah blah', True, BLUE, None)

screen = pygame.display.set_mode(size)

def draw_game(board):
    for r in range(1):
        for c in range(m):
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + 1 + SQUARE_SIZE/2) + SQUARE_SIZE), RADIUS)
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE ))

    for r in range(1,n+1):
        for c in range(m):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE ))
            if board[r-1][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + 1 + SQUARE_SIZE/2)), RADIUS)
            if board[r-1][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + 1 + SQUARE_SIZE/2)), RADIUS)
            if board[r-1][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + 1 + SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()            

board = create_board()
print(board) 
draw_game(board)
pygame.display.update()
game_over = False
turn=0
def get_valid_row(board, col):
    i=n-1
    while i!=-1:
        if board[i][col]==0:
            return i
        i-=1
    # return -1 no row found
    return -1

def is_valid_location(board, col):
    if col >= m or col < 0:
        return -1
    row = get_valid_row(board, col)
    if row == -1:
        return -1
    return row

def check_winner(board, row, col, player):
    counter = 4
    #check vertical
    for i in range(n):
        if board[i][col]==player:
            counter+=1
        else:
            counter=0
        if counter == 4:
            return player

    #check horizontal
    for j in range(m):
        if board[row][j]==player:
            counter+=1
        else:
            counter=0
        if counter == 4:
            return player

    #check diagonal left
    i=max(0,n-m)
    j=max(0,m-n)
    while i < n and j < m:
        if board[i][j]==player:
            counter+=1
        else:
            counter=0
        i+=1
        j+=1
        if counter == 4:
            return player
    
    #check diagonal right
    i = row
    j = col
    while i!=0 and j!=m-1:
        i-=1
        j+=1
    
    while i<n and j>=0:
        if board[i][j] == player:
            counter+=1
        else:
            counter=0
        i+=1
        j-=1
        if counter == 4:
            return player

    return 0



# game loop
while not game_over:
    
    col = -1
    row = -1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            
            posx= event.pos[0]
            if turn%2 == 0:
                pygame.draw.rect(screen, BLACK, (0,0,width, SQUARE_SIZE))
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS )
            else:
                pygame.draw.rect(screen, BLACK, (0,0,width, SQUARE_SIZE))
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS )
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            col = int((event.pos[0]/100)%(m))
            print(col)
            # player 1 turn
            valid_move = 0
            if turn%2 == 0:
                row = is_valid_location(board, col)
                if row == -1:
                    continue
                board[row][col]=1
                #pygame.draw.circle(screen, BLUE, (int(col*SQUARE_SIZE + SQUARE_SIZE/2), int(row*SQUARE_SIZE + 1 + SQUARE_SIZE/2)), RADIUS)
            else: 
                row = is_valid_location(board, col)
                if row == -1:
                    continue
                board[row][col]=2
                #pygame.draw.circle(screen, BLUE, (int(col*SQUARE_SIZE + SQUARE_SIZE/2), int(row*SQUARE_SIZE + 1 + SQUARE_SIZE/2)), RADIUS)
            draw_game(board)
            #check winner
            winner=check_winner(board, row, col, turn%2 + 1)
            turn+=1
            if winner!=0:
                if winner == 1:
                    str = "Player 1 won"
                else:
                    str = "Player 2 won"
                
                label = myfont.render(str, 1, RED)
                screen.blit(label,(40,10))
                
                pygame.time.wait(3000)
                game_over=1

            # board filled
            if turn == n*m:
                label = myfont.render("Game draw", 1, RED)
                pygame.time.wait(3000)
                game_over=1
    draw_game(board)