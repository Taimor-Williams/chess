import pygame
from pygame.sprite import AbstractGroup
from Board_Module import *
import os, sys

# setup constants

pygame.init()
red = (200,0,0)
blue = (0,0,255)
white = (255,255,255)
green = (0,255,00)
orange= (200, 100, 0)

circleX = 100
circleY = 100
radius = 10


WINDOW_HEIGHT = 320
WINDOW_WIDTH = 320
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Chess Project')

# piece group
chessPieceGroup = pygame.sprite.Group()

class PotentialMoves(pygame.sprite.Sprite):
    """
    AF(imgae,rect) = 
    """
    referenceSprite: "ChessPiece"
    image: pygame.Surface 
    referenceIntPiece: int
    newLocation: tuple[int,int]

    def __init__(self, referenceSprite: "ChessPiece", uperLeftSquare: tuple[int,int]) -> None:
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center = uperLeftSquare
        self.referenceSprite = referenceSprite
     

    def isClicked(self, mousePosition: tuple[int,int])->bool:
        """
        @returns true if mouse is colliding with sprite
        """
        mouseX, mouseY = mousePosition
        x,y,width,height = self.image.get_rect()
        x,y = self.rect.center
        x = x -20
        y = y- 20
        # print('Positions')
        # print(mouseX,mouseY)
        # print(x,y)
        if mouseX > x+width or mouseX < x:
            # print('failed')
            return False
        if mouseY > y+height or mouseY < y:
            # print('failed')
            return False
        # print("green square was clicked")
        return True
        

    def clicked(self, gameBoard: Board):
        """
        @param gameBoard, 
        does whatever clicking should do 
        """
        gameBoard.moveObject(self.referenceIntPiece, self.newLocation)

        chessPieceGroup.remove(self.referenceSprite)
        chessPieceGroup.add(ChessPiece(self.piece, newX, newY))
        potentialMovesGroup.empty()
        print(gameBoard.show())

class PotentialCaptures(pygame.sprite.Sprite):
    """
    AF(imgae,rect) = 
    """
    referenceSprite: "ChessPiece"
    image: pygame.Surface 
    referemcePieceInt: int
    newLocation: tuple[int,int]

    def __init__(self, referenceSprite: "ChessPiece", referencePieceInt: int, uperLeftSquare: tuple[int,int]) -> None:
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill(orange)
        self.rect = self.image.get_rect()
        self.rect.center = uperLeftSquare
        self.referemcePieceInt = referencePieceInt
        self.referenceSprite = referenceSprite
     

    def isClicked(self)->bool:
        """
        @returns true if mouse is colliding with sprite
        """
        mouseX, mouseY = pygame.mouse.get_pos()
        x,y,width,height = self.image.get_rect()
        x,y = self.rect.center
        x = x -20
        y = y- 20
        # print('Positions')
        # print(mouseX,mouseY)
        # print(x,y)
        if mouseX > x+width or mouseX < x:
            # print('failed')
            return False
        if mouseY > y+height or mouseY < y:
            # print('failed')
            return False
        # print("green square was clicked")
        return True
        

    def clicked(self, gameBoard: Board):
        """
        @param gameBoard, 
        does whatever clicking should do 
        """
        # print(self.piece.toString())
        # print(self.oldPos)
        # print(self.pos)
        # print(self.oldPos[0]//40, self.oldPos[1]//40)
        # print(self.pos[0]//40, self.pos[1]//40)
        oldX,oldY = self.oldPos[0]//40, self.oldPos[1]//40
        newX,newY = self.pos[0]//40, self.pos[1]//40
        # gameBoard.movementMethod(self.piece, (oldX,oldY), (newX,newY))
        gameBoard.removeObject(oldX,oldY)
        gameBoard.removeObject(newX,newY)
        gameBoard.addObject(self.piece, newX, newY)
        # print("The piece Moved!!!!")
        # print(gameBoard.show())

        chessPieceGroup.remove(self.referenceSprite)
        for chessPiece in chessPieceGroup:
            if chessPiece.rect.center == (newX*40+20,newY*40+20):
                chessPieceGroup.remove(chessPiece)
            break
        chessPieceGroup.add(ChessPiece(self.piece, newX, newY))
        potentialMovesGroup.empty()
        print(gameBoard.show())
        
        

class ChessPiece(pygame.sprite.Sprite):
    """
    AF(imgae,rect) = 
    """
    image: pygame.Surface 
    piece: Piece

    def __init__(self, piece: Piece,x: int,y: int) -> None:
        super().__init__()
        self.image = drawPiece(piece)
        self.rect = self.image.get_rect()
        self.rect.center = (x*40+20,y*40+20)
        self.piece = piece

    def isClicked(self)->bool:
        """
        @returns true if mouse is colliding with sprite
        """
        mouseX, mouseY = pygame.mouse.get_pos()
        # trying to get top left corner as x,y 
        x,y,width,height = self.image.get_rect()
        x,y = self.rect.center
        x = x-20
        y = y-20
        # top left corner is x,y width,height is width/height of rectangle
        # trying to make sure we are inside
        if mouseX > x+width or mouseX < x:
            return False
        if mouseY > y+height or mouseY < y:
            return False
        print(f"method work: {self.piece.toString()}")
        return True
        

    def clicked(self, gameBoard: Board):
        """
        @param gameBoard, 
        does whatever clicking should do 
        """
        x, y = self.rect.center
        x = x-20
        y = y-20
        col,row = convertPosToBoard(x,y,gameBoard)
        # print(f'boardPos, {col,row}')
        # print(f'{self.piece.toString()}')
        (selectPiece, validMoves, validCaptures) = getPieceValidMoves(col,row, gameBoard)
        # print(validMoves, validCaptures)
        drawMoves((x,y), self, self.piece, validMoves, validCaptures)
        
    
potentialMovesGroup = pygame.sprite.Group()

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

def drawGamePieces(boardObject: Board):
    for row in range(boardObject.width):
        for col in range(boardObject.height):
            for gamePiece in boardObject._getLocation(col, row):
                #pygame.Surface.blit(window, drawPiece(gamePiece), [col*rectWidth,row*rectHeight, rectWidth, rectHeight])
                chessPieceGroup.add(ChessPiece(gamePiece, col, row))

def drawMoves(curPos: tuple[int,int], curSprite: ChessPiece, curPiece: Piece, moves: set[tuple[int,int]], captures: set[tuple[int,int]]):
    """
    @params piece,
    @params moves, valid moves you can make
    @params captures, valid captures you can make
    """
    for move in moves:
        x,y = 40*move[0]+20,40*move[1]+20
        potentialMovesGroup.add(PotentialMoves(curPos, curSprite, curPiece,green, x,y))
    for capture in captures:
        x,y = 40*capture[0]+20, 40*capture[1]+20
        potentialMovesGroup.add(PotentialCaptures(curPos, curSprite, curPiece, orange, x,y))


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


class InteractiveGameBoard():
    """
    AF() = 
    """
    gameBoard: Board
    width: int
    heieght: int
    graph: list[list[ChessPiece]]

    def __init__(self, gameBoard: Board) -> None:
        """
        """
        self.gameBoard = gameBoard
        self.width = gameBoard.width
        self.height = gameBoard.height
        self.graph = []
        for graphLoc, square in enumerate(self.gameBoard.graph):
            self.graph.append([])
            for curPiece in square:
                col = graphLoc % self.width
                row = graphLoc // self.width
                self.graph[graphLoc].append(ChessPiece(curPiece, (col,row)))

    def drawSquares():
        """
        @draw gameBoard
        """
    
    def drawPieces():
        """
        """


running=True
gameBoard = Board.parseFromFile('Boards/standard.txt')
frontEndgameBoard = InteractiveGameBoard(gameBoard)

# the ending is the best escape
drawGamePieces(gameBoard)
while running:
    window.fill((0, 0, 0))
    drawBoard(gameBoard)
    # update groups
    potentialMovesGroup.update()
    chessPieceGroup.update()
    # draw sprite groups
    potentialMovesGroup.draw(window)
    chessPieceGroup.draw(window)
    
   
    # events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            print('mousePressed')
            col,row = convertPosToBoard(x,y,gameBoard)
            print(col,row)
            curSprite = frontEndgameBoard.getSprite((col,row))
            if curSprite == None:
                continue
            curSprite.clicked(gameBoard)
            # (selectPiece, validMoves, validCaptures) = getPieceValidMoves(col,row, gameBoard)
            # print(validMoves)
            # print(validCaptures)
            # drawMoves(validMoves,validCaptures)
            # create potentialMoves
            for gamePiece in chessPieceGroup:
                assert(isinstance(gamePiece, ChessPiece) == True)
                if gamePiece.isClicked():
                    gamePiece.clicked(gameBoard)
                    break
            for potentialMove in potentialMovesGroup:
                # assert(isinstance(potentialMove, PotentialMoves) == True)
                if potentialMove.isClicked():
                    print(True)
                    potentialMove.clicked(gameBoard)
                    break
    pygame.display.flip()
pygame.quit()
