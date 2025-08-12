import pygame
from pieces import Piece
import pieces

from typing import Tuple, List, TYPE_CHECKING, Optional,Iterator

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
        rank, file = piece.rank, piece.file
        self.board[rank][file] = piece.id
        self.pieces[piece.id] = piece

    def move_piece_on_board(self, piece_id: str, new_pos: Tuple[int, int]) -> None:
        rank, file = new_pos
        piece = self.get_piece(piece_id)
        self.board[piece.rank][piece.file] = None
        piece.rank, piece.file = new_pos
        self.board[rank][file] = piece_id

    def get_piece_id(self, coords: Tuple[int, int]) -> str | None:
        rank, file = coords
        if not (0 <= rank < self.BOARD_SIZE and 0 <= file < self.BOARD_SIZE):
            return None
        return self.board[rank][file]

    def get_piece(self, piece_id: Optional[str] = None, coords:  Optional[Tuple[int, int]] = None) -> Piece:
        if piece_id:
            return self.pieces[piece_id]
        if coords:
            piece_id = self.get_piece_id(coords)
            if piece_id:
                return self.pieces[piece_id]
            return 

        raise ValueError(
            "Must provide either piece_id or coords to get a piece.")

    def get_all_pieces(self) -> Iterator[Piece]:
        yield from self.pieces.values()


    def remove_piece(self, target_piece_id: str) -> None:
        piece = self.get_piece(target_piece_id)
        self.board[piece.rank][piece.file] = None
        self.pieces.pop(target_piece_id)

    def create_piece(self, piece_type: str, coords: Tuple[int, int], piece_id: List[str], color,game: "Game") -> None:
        if piece_type not in piece_classes:
            raise ValueError(f"Invalid piece type: {piece_type}")
        rank, file = coords

        piece_class = piece_classes[piece_type]
        print(piece_class)
        piece = piece_class(
            (rank, file),
            (game.settings.squarewidth,
             game.settings.squareheight),
            (game.settings.SCREEN_WIDTH,
             game.settings.SCREEN_HEIGHT),
            f"assets/{piece_id[0]}/{piece_type}.png",
            game.settings.padding,
            f"{piece_id[0]}_{piece_type}_{piece_id[1][-1]}",
            color,
            game
        )
        game.players[(game.current_player+1) % 2].pieces.append(piece.id)

    def __str__(self) -> str:
        return "\n".join(str(rank) for rank in self.board)

    def render_board(self, screen: pygame.Surface, size: Tuple[int | float, int | float], tiles: list[pygame.Surface]) -> None:
        width, height = size

        y = 0
        for rank in range(self.BOARD_SIZE):
            x = 0
            for file in range(self.BOARD_SIZE):

                screen.blit(tiles[(rank+file) % 2], (x, y))
                x += width
            y += height
    