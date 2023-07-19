from Piece_Module import *
import copy

def addTuple(tupleOne: tuple[int,int], tupleTwo: tuple[int,int])->tuple[int,int]:
    """
    @param tupleOne
    @param tupleTwo
    @returns stuff 
    """
    x1, y1 = tupleOne
    x2, y2 = tupleTwo
    return (x1+x2,y1+y2)

class Board():
    """
    mutable dataclass
    AF(graph, height, width, internalDict) = a chess board with height "height"
                                            width "width" where for all i,j 0<i<width
                                            0 < j< height, graph[i+j*width] corresponds to 
                                            the objects at location i,j on the board. 
                                            Every object in board or that was ever placed in 
                                            board has a reference number 0<= ref < inf
                                            the reference points to the object in internalDict
    rep invarient():
        len(graph) = height*width
        every object in graph is in internalDict 
    protection from rep exposure():
        constructor():
        Public Functions():
            show(): 
                @returns immutable
            parseBoard():
                @params: immutable string
                @returns: mutable board object
                um is safe though
            parseFromFile():
                @params: str file
                @returns: Board
            getObjects():
                @params tuple[int,int]
                @returns list[int] 
            moveObject(ref, newLoc):
                @param ref, int
                @param newLoc, tuple[int,int]
                item we are moving is never accessed by client
            removeObject(ref)
                @param ref
            addObject(object, loc)
                @param object, object is immutable piece
                @param loc, loc is immutable tuple
            # Algs
            getValidMoves():
                @param int
                @returns set[tuple[int,int]]
                imutable params and returns
            getVaid_captures():
                @paramsint
                @returns set[tuple[int,int]]
                imutable params and returns
        PrivateFunctions():
            # Algs
            movePawn
            _capturePawn
            ..etc

    """
    graph: list[list[Piece]]
    width: int
    height: int
    internalDict: dict[int,"Piece"]

    # public functions
    def __init__(self, width: int, height: int, data: list) -> None:
            self.idGenerator = infiniteSequence()
            self.width = width
            self.height = height
            self.internalDict = {}
            self.graph =[]
            # for col in range(width):
            #     for row in range(height):
            #         self.graph.append([])
            for i in range(0, height*width):
                self.graph.append([])
                col = i % self.width
                row = i // self.width
                objectsatLocation = data[i]
                for addPiece in objectsatLocation:
                    self.addObject(addPiece, (col, row))

    def addObject(self, object: "Piece", location: tuple[int,int]):
        """
        @params object, object we are adding a copy of
        @params location, within the graph
        """
        copyObject = copy.deepcopy(object)
        graphLoc = self._convertColRowToGraphLoc(location)
        curSquare = self.graph[graphLoc]
        curSquare.append(copyObject)
        referenceInt = self._genReferenceInt()
        self.internalDict[referenceInt] = copyObject
    
    def removeObject(self, referenceInt: int):
        """
        @param referenceInt, reference to object in interalDict
        """
        for curLocation in self.graph:
            for i, curObject in enumerate(curLocation):
                curObjectId = self._getReferenceId(curObject)
                if curObjectId == referenceInt:
                    curLocation.pop(i)
                    break

    def moveObject(self, referenceInt: int, newLocation:tuple[int,int]):
        """
        @param referenceInt, int that points to object in internalDict
        @param newLocation, location we are moving object to
        """
        refPiece = self.internalDict[referenceInt]
        curLocation = self._getLocation(refPiece)
        graphLocation = self._convertColRowToGraphLoc(curLocation)
        curSquare = self.graph[graphLocation]

        # remove object from current location
        for i, curPiece in enumerate(curSquare):
            if refPiece == curPiece:
                curSquare.pop(i)
                break
        # adding the object to new location
        newGraphLocation = self._convertColRowToGraphLoc(newLocation)
        self.graph[newGraphLocation].append(refPiece)
    
    def captureObject(self, attackerRef: int, newLocation: tuple[int,int]):
        """
        @param attackRef, piece we are moving
        @param defenferRef, piece we are removing from board
        @param newLocation, location we are moving object to
        """
        refPiece = self.internalDict[attackerRef]
        curLocation = self._getLocation(refPiece)
        graphLocation = self._convertColRowToGraphLoc(curLocation)
        curSquare = self.graph[graphLocation]

        # remove object from current location
        for i, curPiece in enumerate(curSquare):
            if refPiece == curPiece:
                curSquare.pop(i)
                break
        # adding the object to new location
        newGraphLocation = self._convertColRowToGraphLoc(newLocation)
        # removing all objects from new position
        self.graph[newGraphLocation] = []
        self.graph[newGraphLocation].append(refPiece)
        
    def parseBoard(stringBoard: str)-> "Board":
        """
        @param string representation of a board
        @returns said string representation as a board object
        @throws if stringBoard is not a valid board representation
        """
        # fail fast stringBoard is None
        if stringBoard == None:
            raise ValueError
        
        # actual code
        data: list[str] = stringBoard.split()
        sizeString = data.pop(0)
        width,height = sizeString.split("x")
        width, height = int(width), int(height)
        newData: list = [[]]*width*height
        # parsing the data
        for i in range(0, len(data)):
            if data[i] == "empty" or data[i] == "none":
                newData[i] = []
            # black pieces
            if data[i] == "BP":
                newData[i] = [Piece(EnumColors.Black,EnumPieceType.Pawn)]
            if data[i] == "BR":
                newData[i] = [Piece(EnumColors.Black,EnumPieceType.Rook)]
            if data[i] == "BKn":
                newData[i] = [Piece(EnumColors.Black,EnumPieceType.Knight)]
            if data[i] == "BB":
                newData[i] = [Piece(EnumColors.Black,EnumPieceType.Bishop)]
            if data[i] == "BQ":
                newData[i] = [Piece(EnumColors.Black,EnumPieceType.Queen)]
            if data[i] == "BK":
                newData[i] = [Piece(EnumColors.Black,EnumPieceType.King)]
            # white pieces
            if data[i] == "WP":
                newData[i] = [Piece(EnumColors.White,EnumPieceType.Pawn)]
            if data[i] == "WR":
                newData[i] = [Piece(EnumColors.White,EnumPieceType.Rook)]
            if data[i] == "WKn":
                newData[i] = [Piece(EnumColors.White,EnumPieceType.Knight)]
            if data[i] == "WB":
                newData[i] = [Piece(EnumColors.White,EnumPieceType.Bishop)]
            if data[i] == "WQ":
                newData[i] = [Piece(EnumColors.White,EnumPieceType.Queen)]
            if data[i] == "WK":
                newData[i] = [Piece(EnumColors.White,EnumPieceType.King)]
            
            
        return Board(width, height, newData)
    
    def parseFromFile(fileName: str)->"Board":
        """
        @param fileName, IE, 'Boards/standard.txt'
        @returns Board object that corresponds to information in filename
        """
        with open(fileName, 'r') as newFile:
            data = newFile.read()
        return Board.parseBoard(data)

    def show(self)-> str:
        """
        @params void
        @returns a string representation of graph
        example reps: 
            empty board 3x3:
                "empty empty empty
                empty empty empty
                empty empty empty "
            standard chess board 8x8:
                BR    BKn   BB    BQ    BK    BB    BKn   BR
                BP    BP    BP    BP    BP    BP    BP    BP
                empty empty empty empty empty empty empty empty
                empty empty empty empty empty empty empty empty
                empty empty empty empty empty empty empty empty
                empty empty empty empty empty empty empty empty
                WP    WP    WP    WP    WP    WP    WP    WP
                WR    WKn   WB    WQ    WK    WB    WKn   WR
        """
        returnStr:str = ""
        returnStr = f'{self.width}x{self.height}\n'
        for curPosList in self.graph:
            if curPosList == []:
                returnStr = returnStr + "empty\n"
            else:
                for i,curObj in enumerate(curPosList):
                    if issubclass(type(curObj), Piece):
                        returnStr = returnStr + curObj.toString()
                    if i < len(curPosList)-1:
                        returnStr += ','
                returnStr += '\n'
        return returnStr

    def showBetter(self)-> str:
        """
        @params void
        @returns a string representation of graph
        example reps: 
            empty board 3x3:
                "empty empty empty
                empty empty empty
                empty empty empty "
            standard chess board 8x8:
                BR    BKn   BB    BQ    BK    BB    BKn   BR
                BP    BP    BP    BP    BP    BP    BP    BP
                empty empty empty empty empty empty empty empty
                empty empty empty empty empty empty empty empty
                empty empty empty empty empty empty empty empty
                empty empty empty empty empty empty empty empty
                WP    WP    WP    WP    WP    WP    WP    WP
                WR    WKn   WB    WQ    WK    WB    WKn   WR
        """
        returnStr:str = ""
        returnStr = f'{self.width}x{self.height}\n'
        for graphLoc, curPosList in enumerate(self.graph):
            if curPosList == []:
                returnStr = returnStr + "empty\t"
            else:
                for i,curObj in enumerate(curPosList):
                    if issubclass(type(curObj), Piece):
                        returnStr = returnStr + curObj.toString()
                    if i < len(curPosList)-1:
                        returnStr += ','
                returnStr = returnStr +'\t'
            if (graphLoc+1) % self.width == 0:
                returnStr = returnStr+ '\n'
        return returnStr
    
    def getObjects(self, location: tuple[int,int])->list[int]:
        """
        @param location, location in board
        @returns objects, reference Id's for objects at that location
        """
        col,row = location
        locationInGraph = self._convertColRowToGraphLoc((col,row))
        referenceIdList: list[int]= []
        for curPiece in self.graph[locationInGraph]:
            referenceId = self._getReferenceId(curPiece)
            referenceIdList.append(referenceId)
        return referenceIdList

    def showObjects(self, location: tuple[int,int])->list[int]:
        """
        @param location, location in board
        @returns objects, toString of objects at location
        """
        col,row = location
        locationInGraph = self._convertColRowToGraphLoc((col,row))
        showStringList: list[int]= []
        for curPiece in self.graph[locationInGraph]:
            stringPiece = curPiece.toString()
            showStringList.append(stringPiece)
        return showStringList

    def getValidMovesObject(self, referenceInt: int,)-> set[tuple[int,int]]:
        """
        @referenceInt, internalDict reference to piece we are trying to move
        @returns, all validPos piece can move to
        """
        selectPiece = self.internalDict[referenceInt]
        curPos = self._getLocation(selectPiece)

        if selectPiece.pieceType == EnumPieceType.Rook:
            return self._moveRook(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Pawn:
            return self._movePawn(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Bishop:
            return self._moveBishop(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Knight:
            return self._moveKnight(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Queen:
            return self._moveQueen(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.King:
            return self._moveKing(selectPiece, curPos)
    
    def getValidCapturesObject(self, referenceInt: int)-> set[tuple[int,int]]:
        """
        @params referenceInt, internalDict reference to piece we are trying to move
        @returns, all valid _capture positions for selectPiece
        """
        selectPiece = self.internalDict[referenceInt]
        curPos = self._getLocation(selectPiece)

        if selectPiece.pieceType == EnumPieceType.Rook:
            return self._captureRook(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Pawn:
            return self._capturePawn(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Bishop:
            return self._captureBishop(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Knight:
            return self._captureKnight(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.Queen:
            return self._captureQueen(selectPiece, curPos)
        if selectPiece.pieceType == EnumPieceType.King:
            return self._captureKing(selectPiece, curPos)
 
    ###################
    # private functions
    ###################

    def _convertColRowToGraphLoc(self, loc: tuple[int,int]):
        col, row = loc
        return col+row*self.width
    
    def _genReferenceInt(self):
         return next(self.idGenerator)
    
    def _getReferenceId(self, refPiece: Piece)->int:
        for key in self.internalDict:
            curPiece = self.internalDict[key]
            if refPiece == curPiece:
                return key
            
    def _getLocation(self, refPiece: Piece)->tuple[int,int]:
        for index, curLocation in enumerate(self.graph):
            for curPiece in curLocation:
                if refPiece == curPiece:
                    col = index % self.width
                    row = index // self.width
                    return (col,row)
                
    #####################################
    # algs for moving and capturing things
    #####################################

    def _movePawn(self, pawn: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @returns set of valid pos you can move to 
        """
        returnSet = set()
    
    
        if pawn.color == EnumColors.Black:
            # doubleMove
            startCol, startRow = originalPos
            if startRow == 1:
                doubleCol, doubleRow = addTuple(originalPos, (0,2))
                if doubleRow >= 0 and doubleRow <= self.height-1:
                    assert('hi')
                    if doubleCol >= 0 and doubleCol <= self.width-1:
                        assert('hi')
                        location = self._convertColRowToGraphLoc((doubleCol,doubleRow))
                        getObjectsOfPos = self.graph[location]
                        if getObjectsOfPos == []:
                            returnSet.add((doubleCol, doubleRow))
            # regularMove   
            col, row = addTuple(originalPos, (0,1))
            if row < 0 or row > self.height-1:
                assert('hi')
            if col < 0 or col > self.width-1:
                assert('hi')
            location = self._convertColRowToGraphLoc((col,row))
            getObjectsOfPos = self.graph[location]
            if getObjectsOfPos == []:
                returnSet.add(tuple([col,row]))
            
        # double move


        
        if pawn.color == EnumColors.White:
            # doubleMove
            startCol, startRow = originalPos
            if startRow == 6:
                doubleCol, doubleRow = addTuple(originalPos, (0,-2))
                if doubleRow >= 0 and doubleRow <= self.height-1:
                    assert('hi')
                    if doubleCol >= 0 and doubleCol <= self.width-1:
                        assert('hi')
                        location = self._convertColRowToGraphLoc((doubleCol,doubleRow))
                        getObjectsOfPos = self.graph[location]
                        if getObjectsOfPos == []:
                            returnSet.add((doubleCol, doubleRow))
            # regularMove
            col, row = addTuple(originalPos, (0,-1))
            if row < 0 or row > self.height-1:
                assert('hi')
            if col < 0 or col > self.width-1:
                assert('hi')
            location = self._convertColRowToGraphLoc((col,row))
            getObjectsOfPos = self.graph[location]
            if getObjectsOfPos == []:
                returnSet.add(tuple([col,row]))
            
        return returnSet
    
    def _capturePawn(self, pawn: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @returns set of valid pos you can move to 
        """
        returnSet = set()
        if pawn.color == EnumColors.Black:
            for direction in [(1,1), (-1,1)]:
                col, row = addTuple(originalPos, direction)
                if row < 0 or row > self.height-1:
                        continue
                if col < 0 or col > self.width-1:
                        continue
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos != []:
                    potentialCapture = getObjectsOfPos[0]
                    if potentialCapture.color != pawn.color: 
                        returnSet.add(tuple([col,row]))
        
        if pawn.color == EnumColors.White:
           for direction in [(1,-1), (-1,-1)]:
                col, row = addTuple(originalPos, direction)
                if row < 0 or row > self.height-1:
                        continue
                if col < 0 or col > self.width-1:
                        continue
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos != []:
                    potentialCapture = getObjectsOfPos[0]
                    if potentialCapture.color != pawn.color:
                        returnSet.add(tuple([col,row]))
            
        return returnSet
        
    

    def _moveRook(self, rook: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params rook, 
        @params OriginalPos, pos of the piece
        @returns set of valid pos you can move to 
        """
        up = (0,-1)
        down = (0,1)
        left = (-1, 0)
        right =(1, 0)
        directions = [up, down, left, right]
        seenSet = set()
        for direction in directions:
            curPos = originalPos
            getObjectsOfPos = []
            while getObjectsOfPos == []:
                curPos =  addTuple(curPos, direction)
                col, row = curPos
                if row < 0 or row > self.height-1:
                    break
                if col < 0 or col > self.width-1:
                    break
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos == []:
                    seenSet.add(curPos)
                else:
                    break
        return seenSet
    
    def _captureRook(self, rook: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @params rook, rook we are capturing with
        @returns set of valid pos you can _capture on
        """
        up = (0,-1)
        down = (0,1)
        left = (-1, 0)
        right =(1, 0)
        directions = [up, down, left, right]
        seenSet = set()
        for direction in directions:
            curPos = originalPos
            getObjectsOfPos = []
            while getObjectsOfPos == []:
                curPos =  addTuple(curPos, direction)
                col, row = curPos
                if row < 0 or row > self.height-1:
                    break
                if col < 0 or col > self.width-1:
                    break
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos != []:
                    potentialCapture = getObjectsOfPos[0]
                    if potentialCapture.color != rook.color:
                        seenSet.add(curPos)
                    else:
                        break
        return seenSet
    
    def _moveBishop(self, bishop: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
            """
            @params bishop, 
            @params OriginalPos, pos of the piece
            @returns set of valid pos you can move to 
            bishop _moveing position
            """
            upRight = (1,-1)
            downRight = (1,1)
            downLeft = (-1, 1)
            upLeft =(-1, -1)
            directions = [upRight, downRight, downLeft, upLeft]
            seenSet = set()
            for direction in directions:
                curPos = originalPos
                getObjectsOfPos = []
                while getObjectsOfPos == []:
                    curPos =  addTuple(curPos, direction)
                    col, row = curPos
                    if row < 0 or row > self.height-1:
                        break
                    if col < 0 or col > self.width-1:
                        break
                    location = self._convertColRowToGraphLoc((col,row))
                    getObjectsOfPos = self.graph[location]
                    if getObjectsOfPos == []:
                        seenSet.add(curPos)
                    else:
                        break
            return seenSet
    
    def _captureBishop(self, bishop: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
            """
            @params OriginalPos, pos of the piece
            @params bishop, bishop we are moving
            @returns set of valid pos you can _capture on
            """
            upRight = (1,-1)
            downRight = (1,1)
            downLeft = (-1, 1)
            upLeft =(-1, -1)
            directions = [upRight, downRight, downLeft, upLeft]
            seenSet = set()
            for direction in directions:
                curPos =  originalPos
                getObjectsOfPos = []
                while getObjectsOfPos == []:
                    curPos =  addTuple(curPos, direction)
                    col, row = curPos
                    if row < 0 or row > self.height-1:
                        break
                    if col < 0 or col > self.width-1:
                        break
                    location = self._convertColRowToGraphLoc((col,row))
                    getObjectsOfPos = self.graph[location]
                    if getObjectsOfPos != []:
                        potentialCapture = getObjectsOfPos[0]
                        if potentialCapture.color != bishop.color:
                            seenSet.add(curPos)
                        break
            return seenSet
    
    def _moveKnight(self, knight: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @params knight, the knight we are moving
        @returns set of valid pos you can move to 
        """
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        validPositions = set()
        for direction in directions:
            col, row = addTuple(originalPos, direction)
            if row < 0 or row > self.height-1:
                    continue
            if col < 0 or col > self.width-1:
                    continue
            location = self._convertColRowToGraphLoc((col,row))
            getObjectsOfPos = self.graph[location]
            if getObjectsOfPos == []:
                validPositions.add(tuple([col,row]))
        return validPositions
    
    def _captureKnight(self, knight: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @params knight, the knight we are getting valid captures for
        @returns set of valid pos you can move to 
        """
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(1,-2)]
        validPositions = set()
        for direction in directions:
            col, row = addTuple(originalPos, direction)
            if row < 0 or row > self.height-1:
                    continue
            if col < 0 or col > self.width-1:
                    continue
            location = self._convertColRowToGraphLoc((col,row))
            getObjectsOfPos = self.graph[location]
            if getObjectsOfPos != []:
                potentialCapture = getObjectsOfPos[0]
                if potentialCapture.color != knight.color:
                    validPositions.add(tuple([col,row]))
        return validPositions
    
    def _moveQueen(self, queen: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params queen, 
        @params OriginalPos, pos of the piece
        @returns set of valid pos you can move to 
        """
        return self._moveBishop(queen, originalPos).union(self._moveRook(queen, originalPos))
    
    def _captureQueen(self, queen: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @params queen, the queen piece we are capturing with
        @returns set of valid pos you can move to 
        """
        return self._captureBishop(queen, originalPos).union(self._captureRook(queen, originalPos))

    def _moveKing(self, king: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @params king, king piece we are moving
        @returns set of valid pos you can move to 
        """
        returnSet = set()
        for direction in [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]:
                col, row = addTuple(originalPos, direction)
                if row < 0 or row > self.height-1:
                        continue
                if col < 0 or col > self.width-1:
                        continue
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos == []:
                    returnSet.add(tuple([col,row]))
            
        return returnSet
    
    def _captureKing(self, king: Piece, originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @params king, king piece we are checking for potential captures
        @returns set of valid pos you can move to 
        """
        returnSet = set()
        for direction in [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]:
                col, row = addTuple(originalPos, direction)
                if row < 0 or row > self.height-1:
                        continue
                if col < 0 or col > self.width-1:
                        continue
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos != []:
                    potentialCapture = getObjectsOfPos[0]
                    if potentialCapture.color != king.color:
                        returnSet.add(tuple([col,row]))
            
        return returnSet


    def _moveGeneral(self, directions: list[tuple[int,int]], originalPos: tuple[int,int])->set[tuple[int,int]]:
        """
        @params OriginalPos, pos of the piece
        @returns set of valid pos you can move to 
        """
        seenSet = set()
        for direction in directions:
            curPos = originalPos
            getObjectsOfPos = []
            while getObjectsOfPos == []:
                curPos =  addTuple(curPos, direction)
                col, row = curPos
                if row < 0 or row > self.height-1:
                    break
                if col < 0 or col > self.width-1:
                    break
                location = self._convertColRowToGraphLoc((col,row))
                getObjectsOfPos = self.graph[location]
                if getObjectsOfPos == []:
                    seenSet.add(curPos)
                else:
                    break
        return seenSet
    
        
def infiniteSequence():
    num = 0
    while True:
        yield num
        num += 1




