

import pygame


import pieces

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
    def __init__(self, game, color) -> None:
        self.id = color
        self.game = game

        self.start_row = start_row[color]
        self.start_col = 0
        self.pieces = []

        self.selected = False
        self.selected_piece = ""
        self._create_pieces()

    def _create_pieces(self):
        row = self.start_row
        local_piece_map = piece_map[::-1] if self.id == "black" else piece_map
        # local_piece_map = piece_map

        for piece_row in local_piece_map:
            col = 0
            for idx, piece_name in enumerate(piece_row):
                pieceData = piece_name.split('_')
                piece_type = pieceData[0]
                piece_class = piece_classes[piece_type]
                piece_index = ''
                if len(pieceData) == 2:
                    piece_index = pieceData[1]
                if piece_type == "pawn":
                    piece_index = idx

                piece_id = f"{self.id}_{piece_type}{piece_index}"
                piece = piece_class(
                    (row, col), (self.game.settings.squarewidth, self.game.settings.squareheight), (
                        self.game.settings.SCREEN_WIDTH, self.game.settings.SCREEN_HEIGHT),
                    f"assets/{self.id}/{piece_type}.png", self.game.settings.padding, piece_id, self.game)

                self.game.pieces[piece_id] = piece
                self.pieces.append(piece_id)
                # self.game.board[row+1 if self.id ==
                #                 "black" else row][col] = piece_id
                col += 1

            row += 1

    def check_selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return
            print(*self.game.board, sep='\n')

            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = int(mouse_y // self.game.settings.squareheight)
            col = int(mouse_x // self.game.settings.squarewidth)

            if row >=8 or col >=8:
                return
            square = self.game.board[row][col]

            print(f"Row: {row}, Col: {col}")
            print(f"Square: {square}")

            if self.selected and square is None:
                self.game.pieces[self.selected_piece].move_Piece(
                    (row, col), self.pieces)

            if self.selected and square is not None:
                if self.selected_piece == square:
                    self.game.pieces[square].selected = False
                    self.selected_piece = ''
                    self.selected = False
                    self.game.next_moves_surface = None
                    return
                if square in self.pieces:
                    self.game.pieces[self.selected_piece].selected = False
                    self.selected_piece = square
                    self.game.pieces[square].selected = True
                    self.game.pieces[square].make_move_surface()
                    return

                if square not in self.pieces:
                    self.game.pieces[self.selected_piece].kill(
                        (row, col), self.pieces)

            if not self.selected and square is not None:
                if square not in self.pieces:
                    return
                self.game.pieces[square].selected = True
                self.selected_piece = self.game.pieces[square].id
                self.selected = True
                self.game.pieces[square].make_move_surface()
                return
