

import pygame
import pieces


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game


start_row = {
    "black": 0,
    "white": 6
}


piece_classes = {
    "pawn": pieces.Pawn,
    "queen": pieces.Queen,
    "rook": pieces.Rook,
    "bishop": pieces.Bishop,
    "king": pieces.King,
    "knight": pieces.Knight
}


# piece_map = {

#     "pawn": 8,
#     "rook_1": 1,
#     "knight_1": 1,
#     "bishop_1": 1,
#     "queen": 1,
#     "king": 1,
#     "bishop_2": 1,
#     "knight_2": 1,
#     "rook_2": 1
# }


piece_map = [
    ["pawn"] * 8,
    ["rook_1", "knight_1", "bishop_1", "queen",
        "king", "bishop_2", "knight_2", "rook_2"]
]


class Player:
    def __init__(self, game: "Game", color) -> None:
        self.id = color
        self.game = game

        self.start_row = start_row[color]

        self.pieces: list[str] = []

        self.selected = False
        self.selected_piece: str = ""
        self._create_pieces()

    def _create_pieces(self) -> None:
        row = self.start_row
        local_piece_map = piece_map[::-1] if self.id == "black" else piece_map

        for piece_row in local_piece_map:
            for col, piece_name in enumerate(piece_row):
                pieceData = piece_name.split('_')
                piece_type = pieceData[0]
                piece_class = piece_classes[piece_type]
                # Use index for pawns, otherwise use suffix if present
                piece_index = str(col) if piece_type == "pawn" else (
                    pieceData[1] if len(pieceData) == 2 else "")
                piece_id = f"{self.id}_{piece_type}{piece_index}"

                piece = piece_class(
                    (row, col),
                    (self.game.settings.squarewidth, self.game.settings.squareheight),
                    (self.game.settings.SCREEN_WIDTH,
                    self.game.settings.SCREEN_HEIGHT),
                    f"assets/{self.id}/{piece_type}.png",
                    self.game.settings.padding,
                    piece_id,
                    self.game
                )

                self.pieces.append(piece_id)
            row += 1

    def check_selection(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = int(mouse_y // self.game.settings.squareheight)
        col = int(mouse_x // self.game.settings.squarewidth)

        if row >= 8 or col >= 8:
            return

        square = self.game.board.get_piece_id((row, col))
        print(f"Row: {row}, Col: {col}")
        print(f"Square: {square}")

        # If a piece is selected and user clicks an empty square: move
        if self.selected and square is None:
            self.game.board.pieces[self.selected_piece].move_Piece((row, col), self.pieces)
            return

        # If a piece is selected and user clicks a square with a piece
        if self.selected and square is not None:
            # Deselect if clicking the selected piece
            if self.selected_piece == square:
                self.game.board.pieces[square].selected = False
                self.selected_piece = ''
                self.selected = False
                self.game.next_moves_surface = None
                return
            # Switch selection to another of your own pieces
            if square in self.pieces:
                self.game.board.pieces[self.selected_piece].selected = False
                self.selected_piece = square
                self.game.board.pieces[square].selected = True
                self.game.board.pieces[square].make_move_surface()
                return
            # Capture opponent's piece
            if square not in self.pieces:
                self.game.board.pieces[self.selected_piece].kill((row, col), self.pieces)
                return

        # If no piece is selected and user clicks their own piece: select it
        if not self.selected and square is not None and square in self.pieces:
            self.game.board.pieces[square].selected = True
            self.selected_piece = self.game.board.get_piece(square).id
            self.selected = True
            self.game.board.get_piece(square).make_move_surface()
