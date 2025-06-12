import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game  # Adjust the import path if needed


pieces = {
    "pawn": "Pawn",
    "queen": "Queen",
    "rook": "Rook",
    "bishop": "Bishop",
    "king": "King",
    "knight": "Knight"
}


class Piece:
    def __init__(
        self,
        cords: tuple[int, int],
        size: tuple[int | float, int | float],
        screen_size: tuple[int, int],

        texture_url: str,
        padding: int,
        piece_id: str,
        directions: list[str],
        squares: int,
        game: "Game"

    ) -> None:

        # Remember, Row species the Y axis and Col species the X axis.

        # Game reference
        self.game = game

        # Board and position
        self.board = game.board
        self.row, self.col = cords

        # Size and screen
        self.width, self.height = size
        self.screenWidth, self.screenHeight = screen_size

        # Visuals
        self.padding = padding
        self.texture = pygame.image.load(texture_url)
        self.texture = pygame.transform.scale(
            self.texture, (self.width - self.padding, self.height - self.padding))
        self.selected = False

        # Identity
        self.id = piece_id

        # Movement
        self.directions = directions
        self.squares = squares
        self.has_moved = False
        self.valid_moves: list[tuple[int, int]] = []

        print("id", self.id)
        # Place piece on board
        self.game.board.set_piece(self)

    def make_move_surface(self) -> None:
        if not self.valid_moves:
            self.get_validmoves(
                self.game.players[self.game.current_player].pieces)

        move_surface = pygame.Surface(
            (self.screenWidth, self.screenHeight), pygame.SRCALPHA)
        for row, col in self.valid_moves:
            move_surface.blit(self.game.next_move_icon,
                              (col * self.width, row * self.height))
        self.game.next_moves_surface = move_surface

    def get_validmoves(self, team_pieces: list[str]) -> None:
        if self.valid_moves:
            return

        valid_moves = []
        for direction in self.directions:
            dy, dx = self.game.settings.directions[direction]
            next_row, next_col = self.row, self.col
            for _ in range(self.squares):
                next_row += dy
                next_col += dx

                if not (0 <= next_row < 8 and 0 <= next_col < 8):
                    break

                piece_id = self.board.get_piece_id((next_row, next_col))
                if piece_id:
                    if piece_id not in team_pieces:
                        valid_moves.append((next_row, next_col))
                    break

                valid_moves.append((next_row, next_col))
        self.valid_moves = valid_moves

    def highlight_piece(self):
        rect_y = self.row*self.height
        rect_x = self.col*self.width
        rect_w = self.width
        rect_h = self.height
        pygame.draw.rect(
            self.game.screen,
            (255, 255, 0),  # Yellow color
            pygame.Rect(rect_x, rect_y, rect_w, rect_h),
            4  # Thickness of the border
        )

    def render_piece(self) -> None:

        self.game.screen.blit(
            self.texture, (self.col*self.width+self.padding-2, self.row*self.height+self.padding))
        if self.selected:
            self.highlight_piece()

    def move_Piece(self, Pos: tuple[int, int], team_pieces: list[str]) -> bool:
        row, col = Pos

        if not self.valid_moves:
            self.get_validmoves(team_pieces)

        if Pos not in self.valid_moves:
            return False

        self.board.move_piece_on_board(self.id, (row, col))
        self.game.change_turn(self.id)

        self.has_moved = True
        if "pawn" in self.id:
            self.squares = 1
        return True

    def kill(self, Pos: tuple[int, int], team_pieces: list[str]) -> bool:
        if not self.valid_moves:
            self.get_validmoves(team_pieces)
        row, col = Pos
        if (row, col) not in self.valid_moves:
            return False

        if self.board.get_piece_id(
                (row, col)) not in team_pieces:
            target_piece = self.board.get_piece_id(
                (row, col))
            if not target_piece:
                return False
            self.board.remove_piece(target_piece)
            self.move_Piece(Pos, team_pieces)
        return True


class Pawn(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        directions = ["up", "up_left", "up_right"]
        if id.split('_')[0] == 'black':
            directions = ["down", "down_left", "down_right"]
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, directions, 2, game)

    def get_validmoves(self, team_pieces: list[str]) -> None:
        valid_moves = []

        direction = -1 if self.id.startswith("white") else 1

        next_row = self.row + direction
        if 0 <= next_row < 8:

            if self.board.get_piece_id((next_row, self.col)) is None:
                valid_moves.append((next_row, self.col))
                # Two squares forward
                if not self.has_moved:
                    next_row2 = self.row + 2 * direction
                    if 0 <= next_row2 < 8 and self.board.get_piece_id((next_row2, self.col)) is None:
                        valid_moves.append((next_row2, self.col))

            # Captures
            for dc in [-1, 1]:
                next_col = self.col + dc
                if 0 <= next_col < 8:
                    target_id = self.board.get_piece_id((next_row, next_col))
                    if target_id and target_id not in team_pieces:
                        valid_moves.append((next_row, next_col))

        self.valid_moves = valid_moves

    def promote(self):
        row, col = self.row, self.col
        piece_id = self.id.split('_')
        print(piece_id)
        self.board.remove_piece(self.id)
        p_type = "queen"
        # p_type = input("Enter to promote: ")
        self.board.create_piece(p_type, (row, col), piece_id, self.game)

    def move_Piece(self, Pos: tuple[int, int], team_pieces: list[str]) -> bool:
        super().move_Piece(Pos, team_pieces)
        if self.row == 0 or self.row == 7:
            self.promote()

        return True



class Queen(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up", "down", "left", "right",
                                                    "up_left", "up_right", "down_left", "down_right"], 8, game)


class Rook(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up", "down", "left", "right"], 8, game)
        self.directions = ["up", "down", "left", "right"]
        self.squares = 8


class Bishop(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up_left", "up_right", "down_left", "down_right"], 8, game)


class King(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"], 1, game)
        self.directions = ["up", "down", "left", "right",
                           "up_left", "up_right", "down_left", "down_right"]
        self.squares = 1


class Knight(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["knight"], 1, game)

    def get_validmoves(self, team_pieces: list[str]) -> None:
        valid_moves = []
        knight_moves = self.game.settings.directions["knight"]
        for dy, dx in knight_moves:
            next_row = self.row + dy
            next_col = self.col + dx

            if not (0 <= next_row < 8 and 0 <= next_col < 8):
                continue

            piece_id = self.board.get_piece_id((next_row, next_col))
            if piece_id:
                if piece_id not in team_pieces:
                    valid_moves.append((next_row, next_col))
                continue
            valid_moves.append((next_row, next_col))

        self.valid_moves = valid_moves
