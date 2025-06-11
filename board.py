import pygame
from pieces import Piece


class Board:
    def __init__(self, settings) -> None:
        self.board = settings.emptyboard
        self.pieces = {}

    def set_piece(self, piece: Piece) -> None:
        row, col = piece.row, piece.col
        self.board[row][col] = piece.id
        self.pieces[piece.id] = piece

    def move_piece_on_board(self, piece_id: str, new_pos: tuple[int, int]) -> None:
        row, col = new_pos
        piece = self.get_piece(piece_id)
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = new_pos
        self.board[row][col] = piece_id

    def get_piece_id(self, cords: tuple[int, int]) -> str:
        row, col = cords
        if not (0 <= row < 8 and 0 <= col < 8):
            return "Out Of Range"
        return self.board[row][col]

    def get_piece(self, piece_id: str) -> Piece:
        return self.pieces[piece_id]

    def remove_piece(self, target_piece: str) -> None:
        self.pieces.pop(target_piece)

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.board)

    def render_board(self, screen: pygame.Surface, size: tuple[int | float, int | float], tiles: list[pygame.Surface]) -> None:
        width, height = size

        y = 0
        for row in range(8):
            x = 0
            for col in range(1, 9):

                screen.blit(tiles[(row+col) % 2], (x, y))
                x += width
            y += height
