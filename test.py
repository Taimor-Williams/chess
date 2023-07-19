from Piece_Module import *
from Board_Module import *

"""
Testing Strategy 
    Piece():
        constructor():
        # getValidMovesObject():
        #     partition on type of piece:
        #         Pawn, Rook, Knight, etc
        # getValidCapturesObject():
        #     partition on type of piece:
        #         Pawn, Rook, Knight, etc
        toString():
            partition on type of piece:
                Pawn, Rook, Knight, etc

"""

# toString

def test_toString_Pawn():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Pawn)
    assert(newPiece.toString() == "BP")

def test_toString_Rook():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Rook)
    assert(newPiece.toString() == "BR")

def test_toString_Knight():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Knight)
    assert(newPiece.toString() == "BKn")

def test_toString_Bishop():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Bishop)
    assert(newPiece.toString() == "BB")

def test_toString_King():
    newPiece = Piece(EnumColors.Black,EnumPieceType.King)
    assert(newPiece.toString() == "BK")

def test_toString_Queen():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Queen)
    assert(newPiece.toString() == "BQ")

"""
Testing Strategy 
    Board():
        ###############
        Public
        ###############
        constructor:
        parseBoard:
            Empty Board
        show():
            Empty Board
            3x3 board one ShockWave in middle
        addObject():
            partition on: 
        removeObject():
            partition on: empty, nonempty square
        getValidMovesObject():
            partition on pieceType: 
                 Pawn, Rook, Knight, etc
        getValidCapturesObject():
            partition on pieceType: 
                 Pawn, Rook, Knight, etc
            partition on piece:
                piece is same color as capture: yes. no
        ###############
        Private
        ###############
        _genReferenceInt():
            partition on number of times called: 0,1,2

"""
# constructor 

# parse
def test_Board_parse_empty():
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    assert(Board.parseBoard(empty3by3).show() == empty3by3)

def test_Board_parse_Standard():
    newBoard = Board.parseFromFile('Boards/standard.txt')
    assert(newBoard.showObjects((0,0)) == ['BR'])
 
# show
def test_Board_show_empty():
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    assert(empty3by3 == Board.parseBoard(empty3by3).show())

# addObject():
def test_Board_addObject_empty():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,0))
    assert(newBoard.showObjects((1,0))== ["BP"])

# removeObject():
def test_Board_removeObject_Empty():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,0))
    newBoard.addObject(newPiece,(2,0))
    newBoard.removeObject(1)
    assert(newBoard.showObjects((1,0)) == ['BP'])
    assert(newBoard.showObjects((2,0)) == [])
    assert(newBoard.show() == "3x3\nempty\nBP\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n")

def test_Board_removeObject_nonEmpty():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,0))
    newBoard.removeObject(0)
    assert(newBoard.show() == "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n")

# getValidMovesObject():
def test_Board_getValidMovesObject_Pawn():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,1))
    assert(newBoard.getValidMovesObject(0) == set([tuple([0,2])]))

def test_Board_getValidMovesObject_Rook():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Rook)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,1))
    assert(newBoard.getValidMovesObject(0) == set(
        [tuple([0,2]),tuple([0,0]),tuple([1,1]), tuple([2,1])]))

def test_Board_getValidMovesObject_Bishop():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Bishop)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,1))
    assert(newBoard.getValidMovesObject(0) == set(
        [tuple([1,2]),tuple([1,0])]))

def test_Board_getValidMovesObject_Knight_0():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Knight)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,0))
    assert(newBoard.getValidMovesObject(0) == set(
        [tuple([2,1]),tuple([1,2])]))

def test_Board_getValidMovesObject_Knight_1():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Knight)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (1,2))
    assert(newBoard.getValidMovesObject(0)) == set(
        [tuple([0,0]),tuple([2,0])])

def test_Board_getValidMovesObject_Queen():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Queen)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,1))
    assert(newBoard.getValidMovesObject(0) == set(
        [tuple([1,2]),tuple([1,0]),tuple([0,2]),tuple([0,0]),tuple([1,1]), tuple([2,1])]))

def test_Board_getValidMovesObject_King():
    newPiece = Piece(EnumColors.Black,EnumPieceType.King)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,1))
    assert(newBoard.getValidMovesObject(0) == set(
        [tuple([0,0]),tuple([1,0]),tuple([1,1]),tuple([1,2]),tuple([0,2])]))

# getValidCapturesObject():
def test_Board_getValidCapturesObject_Pawn():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,1))
    newBoard.addObject(Piece(EnumColors.White,EnumPieceType.Pawn),(2,2))
    newBoard.addObject(Piece(EnumColors.White,EnumPieceType.Pawn),(0,2))
    
    assert(newBoard.getValidCapturesObject(0)) == set([tuple([2,2]), tuple([0,2])])

def test_Board_getValidCapturesObject_Rook():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Rook)
    enemyPawn = Piece(EnumColors.White,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,1))
    newBoard.addObject(enemyPawn,(0,1))
    assert(newBoard.getValidCapturesObject(0)) == set([tuple([0,1])])

def test_Board_getValidCapturesObject_Bishop():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Bishop)
    enemyPawn = Piece(EnumColors.White,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,1))
    newBoard.addObject(enemyPawn,(0,0))
    assert(newBoard.getValidCapturesObject(0) == set([tuple([0,0])]))
    
def test_Board_getValidCapturesObject_Knight():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Knight)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece, (0,0))
    newBoard.addObject(Piece(EnumColors.White,EnumPieceType.Pawn), (2,1))
    newBoard.addObject(Piece(EnumColors.White,EnumPieceType.Pawn), (1,2))
    assert(newBoard.getValidCapturesObject(0) == set(
        [tuple([2,1]),tuple([1,2])]))

def test_Board_getValidCapturesObject_Queen():
    newPiece = Piece(EnumColors.Black,EnumPieceType.Queen)
    enemyPawn = Piece(EnumColors.White,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,1))
    newBoard.addObject(enemyPawn,(0,1))
    assert(newBoard.getValidCapturesObject(0) == set([tuple([0,1])]))

def test_Board_getValidCapturesObject_King():
    newPiece = Piece(EnumColors.Black,EnumPieceType.King)
    enemyPawn = Piece(EnumColors.White,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(1,1))
    newBoard.addObject(enemyPawn,(0,1))
    assert(newBoard.getValidCapturesObject(0)) == set([tuple([0,1])])

#moveMent method

def test_Board_moveObject():
    newPiece = Piece(EnumColors.White,EnumPieceType.Knight)
    enemyPawn = Piece(EnumColors.White,EnumPieceType.Pawn)
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    newBoard.addObject(newPiece,(0,0))
    # newBoard.addObject(enemyPawn,(1,2))
    newBoard.moveObject(0, (1,2))
    assert(newBoard.showObjects((0,0)) == [])
    assert(newBoard.showObjects((1,2)) == ['WKn'])
    assert(newBoard.internalDict.keys() == set([0]))
    
################
#Private Methods
################

def test_Board_genReferenceInt():
    empty3by3 = "3x3\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\nempty\n"
    newBoard = Board.parseBoard(empty3by3)
    assert (newBoard._genReferenceInt() == 0)
    assert (newBoard._genReferenceInt() == 1)
    assert (newBoard._genReferenceInt() == 2)

###################
# game sim
###################

def test_Game_playerTurn_MovePiece():
    gameBoard = Board.parseFromFile('Boards/standard.txt')
    # see objects
    print(gameBoard.showObjects((0,1)))
    # get object reference
    objectsLocationA7 = gameBoard.getObjects((0,1))
    blackPawnA7Ref = objectsLocationA7[0]
    # get valid moves for object
    blackPawnA7Moves = gameBoard.getValidMovesObject(blackPawnA7Ref)
    # choose the move and move the object
    chosenMove = blackPawnA7Moves.pop()
    gameBoard.moveObject(blackPawnA7Ref, chosenMove)
    # gameBoard.
    assert(gameBoard.showObjects((0,1))==[])
    assert(gameBoard.showObjects((0,2))==['BP'])

def test_Game_playerTurn_CapturePiece():
    gameBoard = Board.parseFromFile('Boards/standard.txt')
    gameBoard.addObject(Piece(EnumColors.White,EnumPieceType.Pawn), (1,2))
    # see objects
    print(gameBoard.showObjects((0,1)))
    # get object reference
    objectsLocationA7 = gameBoard.getObjects((0,1))
    blackPawnA7Ref = objectsLocationA7[0]
    # get valid captures for object
    print(gameBoard.showBetter())
    blackPawnA7Moves = gameBoard.getValidCapturesObject(blackPawnA7Ref)
    # choose the move and move the object
    chosenMove = blackPawnA7Moves.pop()
    gameBoard.captureObject(blackPawnA7Ref, chosenMove)
    # gameBoard.
    print("hey hey hey")
    assert(gameBoard.showObjects((0,1))==[])
    assert(gameBoard.showObjects((1,2))==['BP'])
    print(gameBoard.showBetter())
    
    

