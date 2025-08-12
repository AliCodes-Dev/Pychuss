import pygame

from typing import TYPE_CHECKING, List, Tuple, Set
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
        coords: tuple[int, int],
        size: tuple[int | float, int | float],
        screen_size: tuple[int, int],

        texture_url: str,
        padding: int,
        piece_id: str,
        color: str,
        directions: list[str],
        squares: int,
        game: "Game"

    ) -> None:

        # Remember, rank species the Y axis and file species the X axis.

        # Game reference
        self.game = game

        # Board and position
        self.board = game.board
        self.rank, self.file = coords

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
        self.color = color
        self.type = "base"
        self.checked = False
        self.checking_piece = []

        # Movement
        self.directions = directions
        self.squares = squares
        self.has_moved = False
        self.valid_moves: Set[Tuple[int, int]] = None

        print("id", self.id)
        # Place piece on board
        self.board.set_piece(self)

    def ensure_valid_moves(self, team_pieces, is_king_in_check):

        if self.valid_moves is None:
            self.get_validmoves(team_pieces, is_king_in_check)

    def make_move_surface(self, is_king_in_check) -> None:
        if is_king_in_check and self.type != "king":
            print("King is in check")
            return
        self.ensure_valid_moves(
            self.game.get_current_player().pieces, is_king_in_check)

        move_surface = pygame.Surface(
            (self.screenWidth, self.screenHeight), pygame.SRCALPHA)
        for rank, file in self.valid_moves:
            move_surface.blit(self.game.next_move_icon,
                              (file * self.width, rank * self.height))
        self.game.next_moves_surface = move_surface

    def get_validmoves(self, team_pieces: list[str], is_king_in_check, save: bool = True) -> Tuple:
        
        valid_moves = set()
        danger_sqs = set()
        is_king_spotted = False
        check_by = ""
        for direction in self.directions:
            print("Getting moves for ",direction)
            dy, dx = self.game.settings.directions[direction]
            next_rank, next_file = self.rank, self.file
            for _ in range(self.squares):
                next_rank += dy
                next_file += dx

                if not (0 <= next_rank < 8 and 0 <= next_file < 8):
                    break

                piece = self.board.get_piece(coords=(next_rank, next_file))
                if is_king_spotted:
                    danger_sqs.add((next_rank, next_file))
                    print("KIng was spotted")
                    break

                if piece:
                    if piece.id not in team_pieces:

                        if piece.type == "king":
                            
                            print(self.id, "sees the king")
                            check_by = self.id
                            is_king_spotted = True
                            valid_moves.add((next_rank, next_file))
                            continue
                        valid_moves.add((next_rank, next_file))
                    
                    elif piece.id in team_pieces:
                        danger_sqs.add((next_rank,next_file))
                        print(self.id,"sees friendly pieces")
                    break
                print("Loop didn't break")
                valid_moves.add((next_rank, next_file))
        if save:
            self.valid_moves = valid_moves
            return ()

        valid_moves.update(danger_sqs)
        return valid_moves, check_by

    def highlight_piece(self):
        rect_y = self.rank*self.height
        rect_x = self.file*self.width
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
            self.texture, (self.file*self.width+self.padding-2, self.rank*self.height+self.padding))
        if self.selected:
            self.highlight_piece()

    def move_Piece(self, pos: tuple[int, int], team_pieces: list[str], is_king_in_check: bool) -> bool:
        if is_king_in_check and self.type != "king":
            return False
        rank, file = pos

        self.ensure_valid_moves(team_pieces, is_king_in_check)

        if pos not in self.valid_moves:
            return False

        self.board.move_piece_on_board(self.id, (rank, file))
        self.has_moved = True
        
        
        self.selected = False
        self.game.change_turn()
        self.valid_moves = None
        if self.type == "pawn":
            self.squares = 1
        if self.type == "king":
            self.checked = False
            self.checking_piece.clear()
        return True
    
    def after_move(self):
        pass
    

    

    def capture(self, pos: tuple[int, int], team_pieces: list[str], is_king_in_check: bool) -> bool:
        if is_king_in_check and self.type != "king":
            return False
        self.ensure_valid_moves(team_pieces, is_king_in_check)
        rank, file = pos
        if (rank, file) not in self.valid_moves:
            return False

        if self.board.get_piece_id(
                (rank, file)) not in team_pieces:
            target_piece = self.board.get_piece_id(
                (rank, file))
            if not target_piece:
                return False
            self.board.remove_piece(target_piece)
            self.game.players[(self.game.current_player + 1) %
                              2].pieces.remove(target_piece)
            self.move_Piece(pos, team_pieces, is_king_in_check)

        return True


class Pawn(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        directions = ["up", "up_left", "up_right"]
        if piece_id.split('_')[0] == 'black':
            directions = ["down", "down_left", "down_right"]
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, directions, 2, game)

        self.type = "pawn"

    def get_validmoves(self, team_pieces: list[str], is_king_in_check: bool, save: bool = True) -> Tuple:
        valid_moves = set()
        check_by = ""
        if is_king_in_check and self.type != "king":
            if save:
                self.valid_moves = valid_moves
                return ()
            return valid_moves, check_by

        direction = -1 if self.id.startswith("white") else 1
        next_rank = self.rank + direction
        if 0 <= next_rank < 8:
            # Forward move
            if self.board.get_piece_id((next_rank, self.file)) is None:
                valid_moves.add((next_rank, self.file))
                # Two squares forward from starting position
                if not self.has_moved:
                    next_rank2 = self.rank + 2 * direction
                    if 0 <= next_rank2 < 8 and self.board.get_piece_id((next_rank2, self.file)) is None:
                        valid_moves.add((next_rank2, self.file))
            # Captures
            for dc in [-1, 1]:
                next_file = self.file + dc
                if 0 <= next_file < 8:
                    piece = self.board.get_piece(coords=(next_rank, next_file))
                    if piece and piece.id not in team_pieces:
                        if piece.type == "king":
                            check_by = self.id
                        valid_moves.add((next_rank, next_file))
        if save:
            self.valid_moves = valid_moves
            return ()
        return valid_moves, check_by

    def promote(self):
        rank, file = self.rank, self.file
        piece_id = self.id.split('_')
        print(piece_id)
        self.board.remove_piece(self.id)
        self.game.get_next_player().pieces.remove(self.id)
        
        p_type = "queen"
        
        # p_type = input("Enter to promote: ")
        self.board.create_piece(p_type, (rank, file), piece_id, self.color,self.game)

    def move_Piece(self, pos: tuple[int, int], team_pieces: list[str], is_king_in_check) -> bool:
        super().move_Piece(pos, team_pieces, is_king_in_check)
        if self.rank == 0 or self.rank == 7:
            self.promote()

        return True


class Queen(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up", "down", "left", "right",
                                                                 "up_left", "up_right", "down_left", "down_right"], 8, game)

        self.type = "queen"


class Rook(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up", "down", "left", "right"], 8, game)
        self.directions = ["up", "down", "left", "right"]
        self.squares = 8
        self.type = "rook"


class Bishop(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up_left", "up_right", "down_left", "down_right"], 8, game)
        self.type = "bishop"


class King(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"], 1, game)
        self.directions = ["up", "down", "left", "right",
                           "up_left", "up_right", "down_left", "down_right"]
        self.squares = 1
        self.type = "king"
        self.checked = False
        self.checking_piece = []
        

    def highlight_check(self):

        if not self.checked:
            return
        
        rect_y = self.rank*self.height
        rect_x = self.file*self.width
        rect_w = self.width
        rect_h = self.height
        overlay = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 100))  # Last value is alpha (transparency)
        self.game.screen.blit(overlay, (rect_x, rect_y))

    def render_piece(self) -> None:
        super().render_piece()
        self.highlight_check()
        
    

        


class Knight(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["knight"], 1, game)

        self.type = "knight"

    def get_validmoves(self, team_pieces: list[str], is_king_in_check: bool, save: bool = True) -> Tuple:
        valid_moves = set()
        check_by = ""
        if is_king_in_check and self.type != "king":
            if save:
                self.valid_moves = valid_moves
                return ()
            return valid_moves, check_by

        knight_moves = self.game.settings.directions["knight"]
        for dy, dx in knight_moves:
            next_rank = self.rank + dy
            next_file = self.file + dx
            if not (0 <= next_rank < 8 and 0 <= next_file < 8):
                continue
            piece = self.board.get_piece(coords=(next_rank, next_file))
            if piece and piece.id not in team_pieces:
                if piece.type == "king":
                    check_by = self.id
                valid_moves.add((next_rank, next_file))
            elif not piece:
                valid_moves.add((next_rank, next_file))
        if save:
            self.valid_moves = valid_moves
            return ()
        return valid_moves, check_by


def get_validmoves(self, team_pieces: list[str], save: bool = True) -> Tuple:

    valid_moves = set()
    check_by = ""
    for direction in self.directions:
        dy, dx = self.game.settings.directions[direction]
        next_rank, next_file = self.rank, self.file
        for _ in range(self.squares):
            next_rank += dy
            next_file += dx

            if not (0 <= next_rank < 8 and 0 <= next_file < 8):
                break

            piece = self.board.get_piece(coords=(next_rank, next_file))
            if piece:
                if piece.id not in team_pieces:
                    if piece.type == "king":
                        check_by = self.id
                    valid_moves.add((next_rank, next_file))
                break

            valid_moves.add((next_rank, next_file))
    if save:
        self.valid_moves = valid_moves
        return ()

    return valid_moves, check_by
