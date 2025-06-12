import pygame
from pieces import Piece
import pieces

from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game


piece_classes = {
    "pawn": pieces.Pawn,
    "queen": pieces.Queen,
    "rook": pieces.Rook,
    "bishop": pieces.Bishop,
    "king": pieces.King,
    "knight": pieces.Knight
}


class Board:
    def __init__(self, settings) -> None:
        self.BOARD_SIZE = settings.BOARD_SIZE
        self.board = settings.emptyboard
        self.pieces = {}

    def set_piece(self, piece: Piece) -> None:
        row, col = piece.row, piece.col
        self.board[row][col] = piece.id
        self.pieces[piece.id] = piece

    def move_piece_on_board(self, piece_id: str, new_pos: Tuple[int, int]) -> None:
        row, col = new_pos
        piece = self.get_piece(piece_id)
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = new_pos
        self.board[row][col] = piece_id

    def get_piece_id(self, cords: Tuple[int, int]) -> str | None:
        row, col = cords
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return None
        return self.board[row][col]

    def get_piece(self, piece_id: str) -> Piece:

        return self.pieces[piece_id]

    def remove_piece(self, target_piece_id: str) -> None:
        piece = self.get_piece(target_piece_id)
        self.board[piece.row][piece.col] = None
        self.pieces.pop(target_piece_id)

    def create_piece(self, piece_type: str, cords: Tuple[int, int], piece_id: List[str], game: "Game") -> None:
        if piece_type not in piece_classes:
            raise ValueError(f"Invalid piece type: {piece_type}")
        row, col = cords

        piece_class = piece_classes[piece_type]
        print(piece_class)
        piece = piece_class(
            (row, col),
            (game.settings.squarewidth,
             game.settings.squareheight),
            (game.settings.SCREEN_WIDTH,
             game.settings.SCREEN_HEIGHT),
            f"assets/{piece_id[0]}/{piece_type}.png",
            game.settings.padding,
            f"{piece_id[0]}_{piece_type}_{piece_id[1][-1]}",
            game
        )
        game.players[(game.current_player+1) % 2].pieces.append(piece.id)

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.board)

    def render_board(self, screen: pygame.Surface, size: Tuple[int | float, int | float], tiles: list[pygame.Surface]) -> None:
        width, height = size

        y = 0
        for row in range(self.BOARD_SIZE):
            x = 0
            for col in range(self.BOARD_SIZE):

                screen.blit(tiles[(row+col) % 2], (x, y))
                x += width
            y += height
