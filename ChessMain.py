'''
This is the main driver file. It will be responsible for handling the user input and displaying the current 
GameState object'''

from turtle import Screen
import pygame as p
import ChessEngine
WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #Dimensions of a chess board are 8X8
SQ_SIZE =  HEIGHT // DIMENSION 
MAX_FPS = 15 #For animations later on
IMAGES = {} 

'''
Initialize a global dictionary of images , this will be called exactly once in the main
'''
def loadImages():
    pieces = ['wP' , 'wR' , 'wN' , 'wB' , 'wQ' , 'wK' , 'bP' , 'bR' , 'bN' , 'bB' , 'bQ' , 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    #Note -> We can acces an image by saying 'IMAGES['wp'].'

'''
The main driver code for our program. This will handle the user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Flag variable for when a mve is made

    print(gs.board)
    loadImages() #Only do this once , before the while loop
    running = True
    sqSelected = () #When no square is selected , keep track of the last move of the user(tuple: (row,col))
    playerClicks = [] #Keep track of player clicks (two tuples: [(6, 4), (4,4)])

    while running:
        for e in p.event.get():
            if e.type == p.quit:
                running = False
            #Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #After the second click
                    move = ChessEngine.Move(playerClicks[0] , playerClicks[1] ,   gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True #Update the flag variable
                    sqSelected = () #Reset the user clicks
                    playerClicks = []
            #key handlers   
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True




        DrawGameState(screen , gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible  for all the graphics in the current game state
'''
def DrawGameState(screen , gs):
    drawBoard(screen) #Draw squares on the board
    #add in piece highlighting and move suggestions (later)
    drawPieces(screen , gs.board) #Draw pieces on top of those squares

'''
Draw the squares on the board. The top left square is always light
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen , color , p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the peices on the board using the current game state
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #Not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))








if __name__ == "__main__":
    main()
