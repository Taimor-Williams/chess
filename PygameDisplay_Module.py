import pygame
from pygame.sprite import AbstractGroup
from Board_Module import *
import os, sys

# setup constants

pygame.init()
red = (200,0,0)
blue = (0,0,255)
white = (255,255,255)
green = (0,255,0)
orange= (200, 100, 0)
black = (0,0,0)

circleX = 100
circleY = 100
radius = 10


WINDOW_HEIGHT = 320
WINDOW_WIDTH = 320
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Chess Project')

# piece group
chessPieceGroup = pygame.sprite.Group()


def loadPieces(directory: str)->dict[str,pygame.Surface]:
    """
    @param pieceObject, piece we are drawing
    @returns image bank we can later draw from
    """
    imageDict: dict = {}
    path = os.path.join(os.path.dirname(__file__), "Pieces/"+directory) #stores white pieces images into dicts
    w_dirs = os.listdir(path)
    for file in w_dirs:
        img = pygame.image.load(path+"/"+file)
        img= pygame.transform.scale(img, (40, 40))

        imageDict[file] = img
    return imageDict

# drawing

def drawPiece(piece: Piece)->pygame.surface:
    if piece.color == EnumColors.White:
        imgDict = loadPieces('White')
    if piece.color == EnumColors.Black:
        imgDict = loadPieces('Black')
    return imgDict[piece.toString()+ '.png']

def drawBoard(boardObject: Board):
    """
    @param boardObject, board we are drawing
    """
    rectWidth = 40
    rectHeight = 40 
    for row in range(boardObject.width):
        for col in range(boardObject.height):
            if row % 2 == 0:
                if col % 2 == 0:
                    # print('blue', f'{[col*rectWidth,row*rectHeight, rectWidth, rectHeight]}')
                    pygame.draw.rect(window, blue, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                else:
                    pygame.draw.rect(window, red, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
            else:
                if col % 2 == 0:
                    pygame.draw.rect(window, red, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                else:
                    pygame.draw.rect(window, blue, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
            # # drawing the game piece
            # for gamePiece in boardObject._getLocation(col, row):
            #     print(gamePiece)
            #     #pygame.Surface.blit(window, drawPiece(gamePiece), [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
            #     chessPieceGroup.add(ChessPiece(gamePiece, col, row))



# gameLogic

def convertPosToBoard(x:int, y:int, boardObject: Board)->tuple[int,int]:
    """
    @param x, pos on screen
    @param y, pos on screen
    @returns col,row that matches pos on board
    """
    col = x // 40
    row = y // 40
    return tuple([col,row])

def getPieceValidMoves(col:int,row:int, boardObject: Board):
    """
    @ param col, inside board
    @ param row, inside board
    """
    curList = boardObject._getLocation(col,row)
    if curList != []:
        selectPiece = curList[0]
        validMoves = boardObject.movePiece(selectPiece, (col,row))
        validCaptures = boardObject.capturePiece(selectPiece, (col,row))
        return (selectPiece, validMoves, validCaptures)

# def drawStyleRect(surface):
#     pygame.draw.rect(surface, (0,0,255), (x,y,150,150), 0)
#     for i in range(4):
#         pygame.draw.rect(surface, (0,0,0), (x-i,y-i,155,155), 1)

class InteractiveGameBoard():
    """
    AF(gameBoard, width, height, selected, validCaptureSquares, 
    validMoveSquares, drawDict, referencePieceInt) =  
    a clickable gameboard which displays the chess game. It references the backEnd information 
    in "gameBoard", has width "width", height "height", indicates if a piece is currently selected with
    "selected", displays said selected pieces valid moves in "validMoveSquares",
    displays selected piece valid captures in "validMoveSquares", stores a reference
    to the piece used to move it in the backEnd gameBoard in referencePieceInt, and
    has all the pieces and images stored in "drawDict". 

    rep invarient:
        if selected == False:
            validMoveSquares = []
            validCaptureSquares = []
        
    protection from rep exposure:
        drawSquares():
        drawValidCaptures():
        drawValidMoves():
        drawPieces():
        isClicked():

    """
    gameBoard: Board
    width: int
    height: int
    selected: bool
    validCaptureSquares: list[tuple[int,int]]
    validMoveSquares: list[tuple[int,int]]
    drawDict: dict[str,pygame.Surface]
    referencePieceInt: int


    def __init__(self, gameBoard: Board) -> None:
        """
        """
        self.gameBoard = gameBoard
        self.width = gameBoard.width
        self.height = gameBoard.height
        self.drawDict = loadPieces("White")
        self.drawDict.update(loadPieces('Black'))
        self.validCaptureSquares = []
        self.validMoveSquares = []
        self.selected = False
        self.referencePieceInt = -1


    def drawSquares(self):
        """
        @draw gameBoard
        """
        rectWidth = 40
        rectHeight = 40 
        for row in range(self.width):
            for col in range(self.height):
                if row % 2 == 0:
                    if col % 2 == 0:
                        # print('blue', f'{[col*rectWidth,row*rectHeight, rectWidth, rectHeight]}')
                        pygame.draw.rect(window, blue, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                    else:
                        pygame.draw.rect(window, red, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                else:
                    if col % 2 == 0:
                        pygame.draw.rect(window, red, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                    else:
                        pygame.draw.rect(window, blue, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
    
    def drawValidCaptures(self):
        rectWidth = 40
        rectHeight = 40 
        for location in self.validCaptureSquares:
            col,row = location
            pygame.draw.rect(window, orange, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])


    def drawValidMoves(self):

        rectWidth = 40
        rectHeight = 40 
        for location in self.validMoveSquares:
            col,row = location
            x = col*rectWidth
            y = row*rectHeight
            pygame.draw.rect(window, green, [x,y, rectWidth, rectHeight])
            pygame.draw.rect(window,black, (x,y,rectWidth,rectHeight), 2)

    def drawPieces(self):
        """
        @draw all pieces
        """
        rectWidth = 40
        rectHeight = 40
        for loc, curSquare in enumerate(self.gameBoard.graph):
            col = loc % self.width
            row = loc //self.width
            for gamePiece in curSquare:
                pieceString = gamePiece.toString() + '.png'
                pieceSprite = self.drawDict[pieceString]
                pygame.Surface.blit(window, pieceSprite, [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                

    def isclicked(self, mousePos: tuple[int,int]):
        """
        @param mousePos, 

        """
        x,y = mousePos
        col, row = x//40, y//40
        curSquareLoc = row*self.height+ col
        selectedObjects = self.gameBoard.getObjects((col,row))
        
        # case 1 selected is false

        if not self.selected:
            if selectedObjects == []:
                assert(1==1)
                return
            if selectedObjects != []:
                print("select oject")
                self.selected = True
                referenceObject = selectedObjects[0]
                self.referencePieceInt = referenceObject
                self.validCaptureSquares = self.gameBoard.getValidCapturesObject(referenceObject)
                self.validMoveSquares = self.gameBoard.getValidMovesObject(referenceObject)
                return
        
        # case 2 selected is true
        if self.selected:
            # click on a validMove
            if (col,row) in self.validMoveSquares:
                print("valid move made")
                self.gameBoard.moveObject(self.referencePieceInt, (col,row))
                self.selected = False
                self.validCaptureSquares = []
                self.validMoveSquares = []
                return
            # click on a valid capture
            if (col,row) in self.validCaptureSquares:
                print("valid capture made")
                self.gameBoard.captureObject(self.referencePieceInt, (col,row))
                self.selected = False
                self.validCaptureSquares = []
                self.validMoveSquares = []
                return
            # click on empty square
            if selectedObjects == []:
                print("select empty")
                self.selected = False
                self.validCaptureSquares = []
                self.validMoveSquares = []
                return
            # click on square that has a piece
            if selectedObjects !=[] and self:
                print("select new piece")
                self.selected = False
                self.validCaptureSquares = []
                self.validMoveSquares = []
                return
            
            

            
            

                


                
            


    
    def _getObjectCurSquare(self, curSquareLoc: int):
        curObjectsInSquare = self.graph[curSquareLoc]
        return curObjectsInSquare[0]
        # for object in curSquareLoc:
        #     if isinstance(object, sq)



    


running=True
gameBoard = Board.parseFromFile('Boards/standard.txt')
frontEndgameBoard = InteractiveGameBoard(gameBoard)

# the ending is the best escape

while running:
    window.fill((0, 0, 0))
    frontEndgameBoard.drawSquares()
    frontEndgameBoard.drawValidMoves()
    frontEndgameBoard.drawValidCaptures()
    frontEndgameBoard.drawPieces()

    # events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            print('mousePressed')
            # col,row = convertPosToBoard(x,y,gameBoard)
            # print(col,row)
            frontEndgameBoard.isclicked((x,y))
    pygame.display.flip()
pygame.quit()
