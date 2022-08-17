'''
-> This class is is responsible for storing all the information about the current state of a chess game
-> This will also be responsible for determining the valid moves at the current state. 
-> It will also keep a move log
'''

class GameState():
    def __init__(self):
    #The board here is a 2d array of 8X8 dimensions
    #There are 2 characters for every element 
    #The first character represents the color
    #The second caharcter represents the peices - [R,N,B,Q,K,P]

        self.board = [
            ["bR" , "bN" , "bB" , "bQ" , "bK" , "bB" , "bN" , "bR"],
            ["bP" , "bP" , "bP" , "bP" , "bP" , "bP" , "bP" , "bP"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["wP" , "wP" , "wP" , "wP" , "wP" , "wP" , "wP" , "wP"],
            ["wR" , "wN" , "wB" , "wQ" , "wK" , "wB" , "wN" , "wR"] ]
        self.WhiteToMove = True
        self.movelog = []

    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion and en-passant)
    '''
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #log the move so we can undo it later
        self.WhiteToMove = not self.WhiteToMove #Swap players

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.movelog) != 0: #make sure that there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove =  not self.WhiteToMove #switch turns back

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #the number of rows
            for c in range(len(self.board[r])): #The number of columns in the given row
                turn = self.board[r][c][0]
                if(turn == 'w' and self.WhiteToMove) and (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1] 
                    if piece == 'P':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)
        return moves
        
    def getValidMoves(self):
        return self.getAllPossibleMoves() #Not worry about checks at all
            
    '''
    Get all possible pawn moves and store it in the list if the move is valid
    '''
    def getPawnMoves(self, r,c,moves):
        pass


    '''
    Get all possible rook moves and store it in the list if the move is valid
    '''
    def getRookMoves(self, r,c,moves):
        pass

'''Note:
-> Make a move 
-> Generate all the possible moves for the opposing player
-> Check if the king is checked by any move of the oppoding player
-> If no, then store the move in the list
-> Return the list of valid moves
'''

        
class Move():

    #Maps keys to values
    # key : value
    ranksTORows = {"1":7, "2":6 , "3":5 , "4":4 , 
                   "5":3, "6":2 , "7":1 , "8":0 }
    rowsToRanks = {v:k for k, v in ranksTORows.items()}
    filesToCOls = {"a":0 , "b":1 , "c":2 , "d":3 , "e":4 , "f":5 , "g":6 , "h":7}

    colsToFiles = {v: k for k, v in filesToCOls.items()}

    def __init__(self, startSq , endSq , board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    ''''
Overriding equals method
'''

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        #You can add this to make it like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow , self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


 