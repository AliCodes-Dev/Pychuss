import pygame


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
        id: str,
        directions: list[str],
        squares: int,
        game

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
        self.id = id

        # Movement
        self.directions = directions
        self.squares = squares
        self.has_moved = False
        self.valid_moves = []

        # Place piece on board
        self.board[self.row][self.col] = self.id

    def make_move_surface(self):
        if not self.valid_moves:
            self.get_validmoves(
                self.game.players[self.game.current_player].pieces)
        print("Valid Moves",self.valid_moves)
        move_surface = pygame.Surface(
            (self.screenWidth, self.screenHeight), pygame.SRCALPHA)
        for row, col in self.valid_moves:
            move_surface.blit(self.game.next_move_icon,
                              (col * self.width, row * self.height))
        self.game.next_moves_surface = move_surface

    def get_validmoves(self, team_pieces):
        if self.valid_moves:
            return

        valid_moves = []
        for direction in self.directions:
            next_row = self.row
            next_col = self.col
            dy, dx = self.game.settings.directions[direction]
            for _ in range(self.squares):
                next_row += dy
                next_col += dx

                if not (0 <= next_row < 8 and 0 <= next_col < 8):
                    break
                if self.game.board[next_row][next_col] is not None:
                    target_piece = self.game.board[next_row][next_col]
                    if target_piece not in team_pieces:
                        valid_moves.append((next_row, next_col))

                    break
                valid_moves.append((next_row, next_col))
        self.valid_moves = valid_moves

    def render_piece(self):

        self.game.screen.blit(
            self.texture, (self.col*self.width+self.padding-2, self.row*self.height+self.padding))
        if self.selected:
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

    def move_Piece(self, Pos: tuple, team_pieces, moves=None):
        row, col = Pos

        if not self.valid_moves:
            self.get_validmoves(team_pieces)

        if Pos not in self.valid_moves:
            return

        self.board[self.row][self.col] = None
        self.row, self.col = row, col
        self.board[self.row][self.col] = self.id
        self.selected = False
        self.game.players[self.game.current_player].selected = False
        self.render_piece()
        self.game.current_player = (self.game.current_player + 1) % 2
        self.game.next_moves_surface = None
        self.valid_moves.clear()

        self.has_moved = True
        if "pawn" in self.id:
            self.squares = 1
        return True

    def kill(self, Pos: tuple, team_pieces) -> None:
        if not self.valid_moves:
            self.get_validmoves(team_pieces)

        row, col = Pos
        if self.game.board[row][col] not in team_pieces:
            target_piece = self.game.board[row][col]
            if (row, col) in self.valid_moves:
                self.game.pieces.pop(target_piece)
                self.move_Piece(Pos, team_pieces)


class Pawn(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        directions = ["up", "up_left", "up_right"]
        if id.split('_')[0] == 'black':
            directions = ["down", "down_left", "down_right"]
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, directions, 2, game)

        if self.has_moved:
            self.squares = 1

    def get_validmoves(self, team_pieces):
        valid_moves = []
        for direction in self.directions:
            next_row = self.row
            next_col = self.col
            dx, dy = self.game.settings.directions[direction]
            for _ in range(self.squares):
                next_row += dx
                next_col += dy

                if not (0 <= next_row < 8 and 0 <= next_col < 8):
                    break
                if self.game.board[next_row][next_col] is not None:
                    target_piece = self.game.board[next_row][next_col]
                    if target_piece not in team_pieces and direction not in ["up", "down"]:
                        valid_moves.append((next_row, next_col))
                        break

                    break
                if direction not in ["up", "down"]:
                    continue
                valid_moves.append((next_row, next_col))

        self.valid_moves = valid_moves


class Queen(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"], 8, game)
        self.directions = ["up", "down", "left", "right",
                           "up_left", "up_right", "down_left", "down_right"]
        self.squares = 8


class Rook(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up", "down", "left", "right"], 8, game)
        self.directions = ["up", "down", "left", "right"]
        self.squares = 8


class Bishop(Piece):
    def __init__(self, cords, size, screen_size,  texture_url, padding, id, game):
        super().__init__(cords, size, screen_size,
                         texture_url, padding, id, ["up-left", "up-right", "down-left", "down-right"], 8, game)
        self.directions = ["up_left", "up_right", "down_left", "down_right"]
        self.squares = 8


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
        self.directions = ["knight"]
        self.squares = 1

    def get_validmoves(self, team_pieces):
        valid_moves = []
        knight_moves = self.game.settings.directions["knight"]
        # Knight moves are L-shaped: two squares in one direction and one square perpendicular
        next_row = self.row
        next_col = self.col

        for dy, dx in knight_moves:

            next_row = self.row + dy
            next_col = self.col + dx

            if not (0 <= next_row < 8 and 0 <= next_col < 8):

                continue

            if self.game.board[next_row][next_col] is not None:
                target_piece = self.game.board[next_row][next_col]
                if target_piece not in team_pieces:
                    valid_moves.append((next_row, next_col))

                continue
            valid_moves.append((next_row, next_col))

        self.valid_moves = valid_moves
