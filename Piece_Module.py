from enum import Enum

class EnumColors(Enum):
    """
    valid colors that the pieces can take
    """
    Black = 'B'
    White = 'W'
class EnumPieceType(Enum):
    """
    valid pieceTypes the pieces can have
    """
    Pawn = 'P'
    Rook = 'R'
    Knight = 'Kn'
    Bishop = "B"
    Queen = 'Q'
    King = 'K'


class Piece():
    """
    AF(color,pieceType) = a chess piece of color "color" and type
                        "pieceType". immuatable
    rep invarient():
        true
    protection from rep exposure():
        toString():
            @returns string
    """
    color: EnumColors
    pieceType: EnumPieceType

    def __init__(self, color: EnumColors, pieceType: EnumPieceType) -> None:
        self.color = color
        self.pieceType = pieceType
    
    def toString(self):
        """
        @returns, string reprensation of the piece
        """
        return f'{self.color.value}{self.pieceType.value}'
